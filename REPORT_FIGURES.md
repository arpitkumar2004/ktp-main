# Technical Report Figures & Schematics: KGP Transport Protocol (KTP)
**Course: CS39006 Networks Laboratory | Indian Institute of Technology Kharagpur**

---

## Overview

This document compiles the schematic diagrams, packet layouts, finite state machines, sequence charts, and empirical performance graphs for the KTP (KGP Transport Protocol) technical report.

All figures have been generated as vector schematics (`.svg`) and high-resolution plots (`.png`) in the `figures/` directory.

| Item Label | Title | File Location / Format |
| :--- | :--- | :--- |
| **Figure 1** | Overall System Architecture & Shared Memory IPC Model | [`figures/figure1_architecture.svg`](file:///d:/ktp-main/figures/figure1_architecture.svg) |
| **Table 1** | Packet Frame Wire Specifications for DATA and ACK Datagrams | Formal Table in Report (`tab:packet_format`) |
| **Figure 2** | Protocol Finite State Machine (Sender Transmission Cycle) | [`figures/figure3_state_machine.svg`](file:///d:/ktp-main/figures/figure3_state_machine.svg) |
| **Figure 3** | Sequence Scenario 1: Normal In-Order Transmission & Positive ACK | [`figures/figure4a_normal_transmission.svg`](file:///d:/ktp-main/figures/figure4a_normal_transmission.svg) |
| **Figure 4** | Sequence Scenario 2: Packet Loss & Timeout-Driven Retransmission | [`figures/figure4b_packet_loss.svg`](file:///d:/ktp-main/figures/figure4b_packet_loss.svg) |
| **Figure 5** | Sequence Scenario 3: Lost Acknowledgment & Duplicate Handling | [`figures/figure4c_lost_ack.svg`](file:///d:/ktp-main/figures/figure4c_lost_ack.svg) |
| **Figure 6** | Circular FIFO Buffer Architecture & Queue State Formulas | [`figures/figure5_circular_buffer.svg`](file:///d:/ktp-main/figures/figure5_circular_buffer.svg) |
| **Figure 7** | Experimental Evaluation: Transmission Ratio vs. Drop Probability | [`figures/figure6_performance_graph.png`](file:///d:/ktp-main/figures/figure6_performance_graph.png) |

---

## Figure 1: Overall System Architecture & Shared Memory Model

### Visual Reference
Vector Graphic: [`figures/figure1_architecture.svg`](file:///d:/ktp-main/figures/figure1_architecture.svg)

### Textual / ASCII Schematic
```
+---------------------------------------------------------------------------------------+
|                                USER APPLICATION LAYER                                 |
|                                                                                       |
|   +------------------------------------+     +------------------------------------+   |
|   |       Sender Process (user1.c)     |     |      Receiver Process (user2.c)    |   |
|   |  k_socket(), k_bind(), k_sendto()  |     |  k_socket(), k_bind(), k_recvfrom()|   |
|   +-----------------+------------------+     +------------------+-----------------+   |
+---------------------|-------------------------------------------|---------------------+
                      | Enqueue write_buf                         | Dequeue read_buf
                      v                                           v
+---------------------------------------------------------------------------------------+
|                    SYSTEM V SHARED MEMORY SEGMENT (ftok("/", 'a'))                    |
|                                                                                       |
|   Socket Table: struct k_sock SM[10]                                                  |
|   +--------------------+-----------------------------+----------------------------+   |
|   | Metadata/Addresses | Send Buffer (write_buf)     | Receive Buffer (read_buf)  |   |
|   | fd, src_ip, src_pt | 10 x 512B circular queue    | 10 x 512B circular queue   |   |
|   | dest_ip, dest_port | struct timespec send_time   | Delivers in-order payloads |   |
|   | seq_no, ack_no     | Holds pending messages      | Ready for k_recvfrom()     |   |
|   +--------------------+-----------------------------+----------------------------+   |
+---------------------+-------------------------------------------+---------------------+
                      | Scan sockets & write_buf                  | Write delivered payloads
                      v                                           v
+---------------------------------------------------------------------------------------+
|                           KTP DAEMON PROCESS (ktp_main.c)                             |
|                                                                                       |
|   +------------------------------------+     +------------------------------------+   |
|   |          Sender Thread (S)         |     |         Receiver Thread (R)        |   |
|   | - Wakes up every T/2               |     | - select() multiplexer on UDP fds  |   |
|   | - Checks timeout: now-send_time > T|     | - dropMessage(p) loss simulation   |   |
|   | - Transmits DATA over UDP sendto() |     | - demux: handle_ACK / handle_DATA  |   |
|   +-----------------+------------------+     +------------------+-----------------+   |
+---------------------|-------------------------------------------|---------------------+
                      | UDP sendto()                              | UDP recvfrom()
                      v                                           |
+-----------------------------------------------------------------+---------------------+
|                  UNDERLYING OS UDP / NETWORK LAYER (AF_INET, SOCK_DGRAM)              |
+---------------------------------------------------------------------------------------+
```

### Report Caption & Technical Commentary
> **Figure 1: Architectural decomposition of the KTP transport subsystem.** User processes interface with KTP via library calls that read and write directly to an operating-system-backed POSIX shared memory segment. A decoupled background daemon process hosts dual asynchronous worker threads: Thread S monitors pending buffers and timeout timers, while Thread R multiplexes across all active socket descriptors to receive datagrams, process acknowledgments, and buffer arriving in-order data.

---

## Table 1: Wire Protocol Specifications and Packet Framing

In the technical report, byte-level and bit-level wire specifications are formalized as **Table 1** (rather than a schematic figure) for clear, publication-quality presentation.

### Field Layout Table

| Byte Offset | Bit Field | Datagram Field | Wire Description and In-Memory Accessor |
| :--- | :--- | :--- | :--- |
| **Byte 0** | Bits 0–7 | `FLAG` (8 bits) | Packet type: `0x01` (DATA) or `0x00` (ACK). Accessed via `get_flag()`. |
| **Byte 1** | Bits 8–15 | `SEQ_NO` (8 bits) | Modulo-256 sequence counter $S \in [0, 255]$. Accessed via `get_seq_num()`. |
| **Byte 2** | Bits 16–23 | `ACK_NO` (8 bits) | Cumulative ACK indicating next expected sequence. Accessed via `get_ack_num()`. |
| **Bytes 3 .. $2+L$** | Bits 24 .. $23+8L$ | `PAYLOAD` ($L$ Bytes) | Application payload ($0 \le L \le 512$ bytes). Completely omitted on wire in standalone ACK frames ($L=0$). Accessed via `get_data()`. |

### Datagram Wire Specifications
1. **DATA Packet**: Total Length = $3 + L$ Bytes (Max 515 Bytes)
   - Byte 0: `FLAG = 0x01` (DATA)
   - Byte 1: `SEQ_NO` = Message sequence identifier ($0 \le S \le 255$)
   - Byte 2: `ACK_NO` = Cumulative acknowledgment number
   - Bytes 3 .. $2+L$: Application payload data ($0 \le L \le 512$)

2. **ACK Packet**: Total Length = Exactly 3 Bytes (Fixed)
   - Byte 0: `FLAG = 0x00` (ACK)
   - Byte 1: `SEQ_NO` = Current sequence counter of sender
   - Byte 2: `ACK_NO` = Cumulative sequence number being acknowledged

---

## Figure 2: Protocol Finite State Machine (Sender Transmission Cycle)

### Visual Reference
Vector Graphic: [`figures/figure3_state_machine.svg`](file:///d:/ktp-main/figures/figure3_state_machine.svg)

### Textual / ASCII Schematic
```
             [ START ]
                 |
                 | k_socket() + k_bind()
                 v
      +---------------------+      write_buf not empty      +---------------------+
      |                     | ----------------------------> |                     |
      |  WAITING_FOR_DATA   |    Thread S transmits DATA    |   WAITING_FOR_ACK   |
      |        (0)          |    send_time = now            |         (1)         |
      |                     | <---------------------------- |                     |
      +---------------------+       Valid ACK Received      +---------------------+
                 |              ack_no == (seq_no + 1)%MAX       |           ^
                 |              dequeue(write_buf)               |           | Timeout:
                 | k_close()    seq_no = (seq_no + 1)%MAX        +-----------+ (now - send_time) > T
                 v                                              Retransmit packet
             ((CLOSED))                                         Reset timer
```

### Report Caption & Technical Commentary
> **Figure 2: Finite state machine governing KTP socket transmission.** The sender alternates between two primary states: `WAITING_FOR_DATA` (idle, awaiting application data) and `WAITING_FOR_ACK` (active transmission outstanding). Arrival of a matching positive ACK advances the sequence window and clears the buffer; a timeout triggers retransmission without advancing the sequence number.

---

## Figures 3, 4, 5: Protocol Sequence Diagrams (Scenarios 1, 2, and 3)

### Scenario 1: Normal In-Order Transmission & Positive Acknowledgment (Figure 3)
Visual Reference: [`figures/figure4a_normal_transmission.svg`](file:///d:/ktp-main/figures/figure4a_normal_transmission.svg)

```
Sender (user1)     Sender Daemon (S/R)         Receiver Daemon (R)    Receiver (user2)
      |                     |                           |                    |
      | 1. k_sendto()       |                           |                    |
      |-------------------->| (Enqueued in write_buf)   |                    |
      |                     |                           |                    |
      |                     | 2. UDP sendto(): DATA     |                    |
      |                     |    [Seq=1, Ack=1, "hello"]|                    |
      |                     |-------------------------->|                    |
      |                     | (send_time = now;         | dropMessage(p)=0   |
      |                     |  state=WAITING_FOR_ACK)   | (In-order payload  |
      |                     |                           |  queued in read_buf|
      |                     |                           |  ack_no set to 2)  |
      |                     |                           |                    |
      |                     | 3. UDP sendto(): ACK      |                    |
      |                     |    [Seq=1, Ack=2]         |                    |
      |                     |<--------------------------|                    |
      |                     | (Valid ACK: seq_no=2;     |                    |
      |                     |  dequeue write_buf;       |                    |
      |                     |  state=WAITING_FOR_DATA)  |                    |
      |                     |                           | 4. k_recvfrom()    |
      |                     |                           |<-------------------|
      |                     |                           | (Returns "hello")  |
      |                     |                           |------------------->|
```

---

### Scenario B: Packet Loss & Timeout-Driven Retransmission
Visual Reference: [`figures/figure4b_packet_loss.svg`](file:///d:/ktp-main/figures/figure4b_packet_loss.svg)

```
Sender (user1)     Sender Daemon (S/R)         Receiver Daemon (R)    Receiver (user2)
      |                     |                           |                    |
      | 1. k_sendto()       |                           |                    |
      |-------------------->| (Enqueued in write_buf)   |                    |
      |                     |                           |                    |
      |                     | 2. UDP sendto(): DATA     |                    |
      |                     |    [Seq=1, "hello"]       |                    |
      |                     |-----------\ (Loss event)  |                    |
      |                     |            X dropMsg(p)=1 |                    |
      |                     |                           |                    |
      |                     | [Timer Running: T = 2.0s] |                    |
      |                     | . . .                     |                    |
      |                     | TIMEOUT EXPIRED!          |                    |
      |                     | (now - send_time) > T     |                    |
      |                     |                           |                    |
      |                     | 3. RETRY: DATA [Seq=1]    |                    |
      |                     |-------------------------->|                    |
      |                     | (send_time reset)         | dropMessage(p)=0   |
      |                     |                           | (Enqueued to buf;  |
      |                     |                           |  ack_no set to 2)  |
      |                     |                           |                    |
      |                     | 4. UDP sendto(): ACK      |                    |
      |                     |    [Seq=1, Ack=2]         |                    |
      |                     |<--------------------------|                    |
      |                     | (Valid ACK: seq_no=2;     |                    |
      |                     |  dequeue write_buf;       |                    |
      |                     |  state=WAITING_FOR_DATA)  |                    |
```

---

### Scenario 2: Packet Loss & Timeout-Driven Retransmission (Figure 4)
Visual Reference: [`figures/figure4b_packet_loss.svg`](file:///d:/ktp-main/figures/figure4b_packet_loss.svg)

```
Sender (user1)     Sender Daemon (S/R)         Receiver Daemon (R)    Receiver (user2)
      |                     |                           |                    |
      | 1. k_sendto()       |                           |                    |
      |-------------------->| (Enqueued in write_buf)   |                    |
      |                     |                           |                    |
      |                     | 2. UDP sendto(): DATA     |                    |
      |                     |    [Seq=1, "hello"]       |                    |
      |                     |-----------\ (Loss event)  |                    |
      |                     |            X dropMsg(p)=1 |                    |
      |                     |                           |                    |
      |                     | [Timer Running: T = 2.0s] |                    |
      |                     | . . .                     |                    |
      |                     | TIMEOUT EXPIRED!          |                    |
      |                     | (now - send_time) > T     |                    |
      |                     |                           |                    |
      |                     | 3. RETRY: DATA [Seq=1]    |                    |
      |                     |-------------------------->|                    |
      |                     | (send_time reset)         | dropMessage(p)=0   |
      |                     |                           | (Enqueued to buf;  |
      |                     |                           |  ack_no set to 2)  |
      |                     |                           |                    |
      |                     | 4. UDP sendto(): ACK      |                    |
      |                     |    [Seq=1, Ack=2]         |                    |
      |                     |<--------------------------|                    |
      |                     | (Valid ACK: seq_no=2;     |                    |
      |                     |  dequeue write_buf;       |                    |
      |                     |  state=WAITING_FOR_DATA)  |                    |
```

---

### Scenario 3: Lost Acknowledgment & Duplicate Packet Handling (Figure 5)
Visual Reference: [`figures/figure4c_lost_ack.svg`](file:///d:/ktp-main/figures/figure4c_lost_ack.svg)

```
Sender (user1)     Sender Daemon (S/R)         Receiver Daemon (R)    Receiver (user2)
      |                     |                           |                    |
      | 1. k_sendto()       |                           |                    |
      |-------------------->| (Enqueued in write_buf)   |                    |
      |                     |                           |                    |
      |                     | 2. Initial DATA [Seq=1]   |                    |
      |                     |-------------------------->|                    |
      |                     |                           | (Stored in read_buf|
      |                     |                           |  ack_no set to 2)  |
      |                     |                           |                    |
      |                     | 3. ACK [Seq=1, Ack=2]     |                    |
      |                     |             X (ACK lost!) |                    |
      |                     |<-----------/              |                    |
      |                     |                           |                    |
      |                     | [Timer expires after T]   |                    |
      |                     |                           |                    |
      |                     | 4. Duplicate DATA [Seq=1] |                    |
      |                     |-------------------------->|                    |
      |                     |                           | DUPLICATE DETECTED!|
      |                     |                           | Seq 1 < ack_no 2   |
      |                     |                           | -> Discard payload |
      |                     |                           |                    |
      |                     | 5. Re-send ACK(Ack=2)     |                    |
      |                     |<--------------------------|                    |
      |                     | (ACK received; sender     |                    |
      |                     |  clears write_buf)        | 6. k_recvfrom()    |
      |                     |                           |<-------------------|
      |                     |                           | (Single "hello")   |
      |                     |                           |------------------->|
```

### Report Caption & Technical Commentary
> **Figures 3, 4, 5: Protocol timing and sequence interactions.** Figure 3 portrays the nominal Stop-and-Wait handshake. Figure 4 demonstrates recovery from forward loss via sender timer expiry and retransmission. Figure 5 demonstrates resilience to reverse acknowledgment loss: the receiver detects the duplicate sequence number, discards redundant payload data, and retransmits the cumulative ACK to release the sender.

---

## Figure 6: Circular Buffer & Queue State Layout

### Visual Reference
Vector Graphic: [`figures/figure5_circular_buffer.svg`](file:///d:/ktp-main/figures/figure5_circular_buffer.svg)

### Textual / ASCII Schematic
```
Slot Array: char data[10][512] (Capacity: BUF_SIZE = 10)

   [0]       [1]       [2]       [3]       [4]       [5]       [6]       [7]       [8]       [9]
+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
|  Empty  |  Empty  | Msg #1  | Msg #2  | Msg #3  | Msg #4  |  Empty  |  Empty  |  Empty  |  Empty  |
|         |         |  512B   |  512B   |  512B   |  512B   |         |         |         |         |
+---------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
                         ^                             ^
                         |                             |
                       front = 2                     back = 5
                    (Dequeue point)               (Last enqueued)

Queue Invariants & Algebraic Formulations:
1. Empty Condition : front == (back + 1) % BUF_SIZE
2. Full Condition  : front == (back + 2) % BUF_SIZE
3. Enqueue Action  : back = (back + 1) % BUF_SIZE; memcpy(data[back], msg, 512)
4. Dequeue Action  : front = (front + 1) % BUF_SIZE
```

### Report Caption & Technical Commentary
> **Figure 6: Circular queue buffer layout and boundary conditions.** Bounded FIFO storage prevents dynamic memory allocation overhead during runtime. The empty and full invariants guarantee that buffer wrap-around is managed without race conditions or memory fragmentation.

---

## Figure 7: Experimental Performance Evaluation

### Visual Reference
Image File: [`figures/figure6_performance_graph.png`](file:///d:/ktp-main/figures/figure6_performance_graph.png)  
Vector File: [`figures/figure6_performance_graph.svg`](file:///d:/ktp-main/figures/figure6_performance_graph.svg)

### Data Points Plotted

| Drop Probability ($p$) | Observed Transmissions per Message | Theoretical Lower Bound $\frac{1}{1 - p}$ | Theoretical Bidirectional $\frac{1}{(1 - p)^2}$ |
| :---: | :---: | :---: | :---: |
| **0.05** | 2.7 | 1.05 | 1.11 |
| **0.10** | 1.1 | 1.11 | 1.23 |
| **0.15** | 1.7 | 1.18 | 1.38 |
| **0.20** | 1.6 | 1.25 | 1.56 |
| **0.25** | 2.1 | 1.33 | 1.78 |
| **0.30** | 3.6 | 1.43 | 2.04 |
| **0.40** | 1.7 | 1.67 | 2.78 |
| **0.50** | 3.2 | 2.00 | 4.00 |

### Report Caption & Technical Commentary
> **Figure 7: Average number of transmissions per message as a function of simulated packet drop probability ($p$).** The empirical measurements (solid blue squares) reflect the retransmission overhead incurred under varying channel error rates. The experimental curve tracks between the single-link geometric expectation ($1 / (1-p)$) and the bidirectional loss curve ($1 / (1-p)^2$), validating the robustness of the timeout and retransmission engine across synthetic loss conditions up to $p = 0.50$.
