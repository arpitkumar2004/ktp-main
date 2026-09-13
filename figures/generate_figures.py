import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure output directory exists
os.makedirs("figures", exist_ok=True)

# ----------------------------------------------------------------------
# FIGURE 6: Experimental Performance Graph
# ----------------------------------------------------------------------
def generate_figure6():
    probabilities = np.array([0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50])
    transmissions = np.array([2.7, 1.1, 1.7, 1.6, 2.1, 3.6, 1.7, 3.2])

    # Theoretical geometric distribution expectation: 1 / (1 - p)
    p_theory = np.linspace(0.01, 0.52, 100)
    trans_theory_single = 1.0 / (1.0 - p_theory)
    trans_theory_both = 1.0 / ((1.0 - p_theory) ** 2)

    plt.figure(figsize=(9, 5.6), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    # Plot theoretical baselines
    plt.plot(p_theory, trans_theory_single, label='Theoretical Lower Bound: 1 / (1 - p)', 
             color='#64748b', linestyle='--', linewidth=1.8, alpha=0.85)
    plt.plot(p_theory, trans_theory_both, label='Theoretical Bidirectional Loss: 1 / (1 - p)^2', 
             color='#d97706', linestyle=':', linewidth=2.0, alpha=0.9)

    # Plot empirical measurements
    plt.plot(probabilities, transmissions, label='Empirical Measurements (KTP Prototype)', 
             color='#2563eb', marker='s', markersize=7.5, linewidth=2.4, zorder=5)

    # Annotate empirical points with distinct non-overlapping background boxes
    custom_offsets = {
        0.05: (0, 11),
        0.10: (0, -18),
        0.15: (-10, 12),
        0.20: (10, -18),
        0.25: (0, 11),
        0.30: (0, 11),
        0.40: (0, 11),
        0.50: (0, 11),
    }
    for p, t in zip(probabilities, transmissions):
        ox, oy = custom_offsets.get(p, (0, 11))
        plt.annotate(
            f"{t:.1f}", (p, t), textcoords="offset points", xytext=(ox, oy),
            ha='center', fontsize=9, fontweight='bold', color='#1e3a8a',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffffff', edgecolor='#94a3b8', linewidth=0.8, alpha=0.95)
        )

    plt.title('KTP Evaluation: Average Transmissions per Message vs. Packet Drop Probability (p)', 
              fontsize=12, fontweight='bold', pad=15)
    plt.xlabel('Simulated Packet Drop Probability (p)', fontsize=11, fontweight='semibold')
    plt.ylabel('Average Transmissions per Message (#Tx / #Msg)', fontsize=11, fontweight='semibold')
    plt.xlim(0.0, 0.55)
    plt.ylim(0.5, 4.6)
    plt.xticks(np.arange(0.0, 0.55, 0.05))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(frameon=True, facecolor='white', edgecolor='#cbd5e1', framealpha=0.95, loc='upper left', fontsize=9.5)
    plt.tight_layout()

    plt.savefig('figures/figure6_performance_graph.png', dpi=300)
    plt.savefig('figures/figure6_performance_graph.svg')
    plt.close()
    print("Generated figure6_performance_graph.png and figure6_performance_graph.svg")


# ----------------------------------------------------------------------
# FIGURE 1: Overall System Architecture & Shared Memory Model (SVG)
# ----------------------------------------------------------------------
def generate_figure1():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 680" width="100%" height="100%" style="font-family: Arial, sans-serif; background-color: #ffffff;">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b" />
    </marker>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#d97706" />
    </marker>
    <filter id="box-shadow" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#0f172a" flood-opacity="0.06" />
    </filter>
  </defs>

  <!-- Title -->
  <text x="480" y="32" text-anchor="middle" font-size="17" font-weight="bold" fill="#1e293b">Figure 1: KTP System Architecture and Inter-Process Communication Model</text>

  <!-- Layer 1: Application Space -->
  <rect x="40" y="55" width="880" height="115" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
  <text x="55" y="78" font-size="12" font-weight="bold" fill="#475569">USER APPLICATION LAYER (POSIX Process Isolation)</text>

  <!-- user1.c box -->
  <rect x="70" y="92" width="380" height="64" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" filter="url(#box-shadow)" />
  <text x="260" y="117" text-anchor="middle" font-size="14" font-weight="bold" fill="#1d4ed8">Sender Process (user1.c)</text>
  <text x="260" y="137" text-anchor="middle" font-size="11" fill="#3b82f6">API Calls: k_socket(), k_bind(), k_sendto(), k_close()</text>

  <!-- user2.c box -->
  <rect x="510" y="92" width="380" height="64" rx="6" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5" filter="url(#box-shadow)" />
  <text x="700" y="117" text-anchor="middle" font-size="14" font-weight="bold" fill="#15803d">Receiver Process (user2.c)</text>
  <text x="700" y="137" text-anchor="middle" font-size="11" fill="#16a34a">API Calls: k_socket(), k_bind(), k_recvfrom(), k_close()</text>

  <!-- IPC Connection Lines (Apps to Shared Memory) -->
  <line x1="260" y1="156" x2="260" y2="212" stroke="#2563eb" stroke-width="2.2" marker-end="url(#arrow-blue)" />
  <rect x="125" y="174" width="120" height="20" rx="3" fill="#ffffff" stroke="#93c5fd" stroke-width="1" />
  <text x="185" y="188" text-anchor="middle" font-size="10" fill="#1d4ed8" font-weight="bold">Enqueue write_buf</text>

  <line x1="700" y1="212" x2="700" y2="162" stroke="#16a34a" stroke-width="2.2" marker-end="url(#arrow-green)" />
  <rect x="715" y="174" width="120" height="20" rx="3" fill="#ffffff" stroke="#86efac" stroke-width="1" />
  <text x="775" y="188" text-anchor="middle" font-size="10" fill="#15803d" font-weight="bold">Dequeue read_buf</text>

  <!-- Layer 2: Shared Memory -->
  <rect x="40" y="218" width="880" height="160" rx="8" fill="#fffbeb" stroke="#f59e0b" stroke-width="1.8" />
  <text x="55" y="242" font-size="12" font-weight="bold" fill="#b45309">SYSTEM V SHARED MEMORY SEGMENT (ftok("/", 'a'))</text>

  <!-- k_sock Table representation -->
  <rect x="70" y="254" width="820" height="110" rx="6" fill="#ffffff" stroke="#fcd34d" stroke-width="1.2" />
  <text x="480" y="274" text-anchor="middle" font-size="12.5" font-weight="bold" fill="#92400e">Socket Table: struct k_sock SM[SHM_SIZE = 10]</text>

  <!-- Table details: 3 non-overlapping cards -->
  <rect x="90" y="286" width="240" height="66" rx="4" fill="#fef3c7" stroke="#f59e0b" stroke-width="1" />
  <text x="210" y="306" text-anchor="middle" font-size="11" font-weight="bold" fill="#78350f">Metadata &amp; Addressing</text>
  <text x="210" y="323" text-anchor="middle" font-size="10" fill="#451a03">fd, src_ip, src_port, dest_ip, dest_port</text>
  <text x="210" y="339" text-anchor="middle" font-size="10" fill="#451a03">seq_no, ack_no, state flags</text>

  <rect x="360" y="286" width="240" height="66" rx="4" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.2" />
  <text x="480" y="306" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">Send Buffer (write_buf)</text>
  <text x="480" y="323" text-anchor="middle" font-size="10" fill="#172554">queue write_buf (10 × 512B slots)</text>
  <text x="480" y="339" text-anchor="middle" font-size="10" fill="#172554">struct timespec send_time (timer)</text>

  <rect x="630" y="286" width="240" height="66" rx="4" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.2" />
  <text x="750" y="306" text-anchor="middle" font-size="11" font-weight="bold" fill="#166534">Receive Buffer (read_buf)</text>
  <text x="750" y="323" text-anchor="middle" font-size="10" fill="#052e16">queue read_buf (10 × 512B slots)</text>
  <text x="750" y="339" text-anchor="middle" font-size="10" fill="#052e16">Holds delivered in-order payload</text>

  <!-- Connectors from SHM to Daemon -->
  <line x1="260" y1="378" x2="260" y2="422" stroke="#d97706" stroke-width="2.2" marker-end="url(#arrow-orange)" />
  <line x1="700" y1="422" x2="700" y2="384" stroke="#d97706" stroke-width="2.2" marker-end="url(#arrow-orange)" />

  <!-- Layer 3: Daemon Engine (ktp_main) -->
  <rect x="40" y="428" width="880" height="140" rx="8" fill="#f8fafc" stroke="#64748b" stroke-width="1.5" />
  <text x="55" y="450" font-size="12" font-weight="bold" fill="#334155">KTP PROTOCOL DAEMON (ktp_main.c Background Process)</text>

  <!-- Thread S -->
  <rect x="70" y="462" width="380" height="92" rx="6" fill="#f0f9ff" stroke="#0ea5e9" stroke-width="1.5" filter="url(#box-shadow)" />
  <text x="260" y="484" text-anchor="middle" font-size="13" font-weight="bold" fill="#0369a1">Sender Thread (S)</text>
  <text x="260" y="503" text-anchor="middle" font-size="10" fill="#0f172a">• Periodic sleep(T/2); scans active sockets in SM</text>
  <text x="260" y="519" text-anchor="middle" font-size="10" fill="#0f172a">• If WAITING_FOR_ACK &amp; (now - send_time &gt; T): Retransmit</text>
  <text x="260" y="535" text-anchor="middle" font-size="10" fill="#0f172a">• If WAITING_FOR_DATA &amp; !empty(write_buf): Transmit DATA</text>

  <!-- Thread R -->
  <rect x="510" y="462" width="380" height="92" rx="6" fill="#faf5ff" stroke="#8b5cf6" stroke-width="1.5" filter="url(#box-shadow)" />
  <text x="700" y="484" text-anchor="middle" font-size="13" font-weight="bold" fill="#6d28d9">Receiver Thread (R)</text>
  <text x="700" y="503" text-anchor="middle" font-size="10" fill="#0f172a">• I/O Multiplexing across sockets via select()</text>
  <text x="700" y="519" text-anchor="middle" font-size="10" fill="#0f172a">• Simulated packet drop filter: dropMessage(p)</text>
  <text x="700" y="535" text-anchor="middle" font-size="10" fill="#0f172a">• Demux: handle_ACK (dequeue) vs. handle_DATA (ACK + buffer)</text>

  <!-- Network Layer Lines -->
  <line x1="260" y1="554" x2="260" y2="596" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arrow)" />
  <rect x="140" y="565" width="105" height="19" rx="3" fill="#ffffff" stroke="#7dd3fc" stroke-width="1" />
  <text x="192" y="579" text-anchor="middle" font-size="10" fill="#0369a1" font-weight="bold">sendto() UDP</text>

  <line x1="700" y1="596" x2="700" y2="560" stroke="#7c3aed" stroke-width="2.2" marker-end="url(#arrow)" />
  <rect x="715" y="565" width="105" height="19" rx="3" fill="#ffffff" stroke="#c4b5fd" stroke-width="1" />
  <text x="767" y="579" text-anchor="middle" font-size="10" fill="#6d28d9" font-weight="bold">recvfrom() UDP</text>

  <!-- Layer 4: Physical / OS Transport Layer -->
  <rect x="40" y="602" width="880" height="56" rx="8" fill="#1e293b" stroke="#0f172a" stroke-width="1.5" />
  <text x="480" y="636" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">UNDERLYING OS UDP / IP LAYER (AF_INET, SOCK_DGRAM)</text>
</svg>'''
    with open('figures/figure1_architecture.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Generated figure1_architecture.svg")





# ----------------------------------------------------------------------
# FIGURE 3: Protocol Finite State Machine (SVG)
# ----------------------------------------------------------------------
def generate_figure3():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 520" width="100%" height="100%" style="font-family: Arial, sans-serif; background-color: #ffffff;">
  <defs>
    <marker id="fsm-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b" />
    </marker>
    <marker id="fsm-arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb" />
    </marker>
    <marker id="fsm-arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
    </marker>
    <marker id="fsm-arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626" />
    </marker>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.07" />
    </filter>
  </defs>

  <!-- Title -->
  <text x="480" y="32" text-anchor="middle" font-size="17" font-weight="bold" fill="#1e293b">Figure 3: KTP Socket Finite State Machine (Sender Transmission Cycle)</text>

  <!-- Initial / Start State -->
  <circle cx="80" cy="215" r="16" fill="#1e293b" />
  <text x="80" y="250" text-anchor="middle" font-size="11" font-weight="bold" fill="#475569">START</text>

  <!-- Transition 1: k_socket() + k_bind() -->
  <line x1="96" y1="215" x2="190" y2="215" stroke="#1e293b" stroke-width="2" marker-end="url(#fsm-arrow)" />
  <rect x="105" y="174" width="76" height="34" rx="3" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" />
  <text x="143" y="188" text-anchor="middle" font-size="10" font-weight="bold" fill="#1e293b">k_socket()</text>
  <text x="143" y="201" text-anchor="middle" font-size="9" fill="#475569">k_bind()</text>

  <!-- State 0: WAITING_FOR_DATA -->
  <g transform="translate(195, 150)">
    <rect x="0" y="0" width="230" height="135" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="2" filter="url(#shadow)" />
    <rect x="0" y="0" width="230" height="34" rx="8" fill="#2563eb" />
    <text x="115" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">WAITING_FOR_DATA (0)</text>
    <text x="15" y="56" font-size="10.5" fill="#1e293b">• Socket idle / buffer ready</text>
    <text x="15" y="75" font-size="10.5" fill="#1e293b">• Accepts k_sendto() into write_buf</text>
    <text x="15" y="94" font-size="10.5" fill="#1e293b">• Peer DATA packets received</text>
    <text x="15" y="112" font-size="10.5" fill="#1e293b">  and acknowledged immediately</text>
  </g>

  <!-- Upper Transition Path: Send DATA (Curved upwards) -->
  <path d="M 425 175 C 475 105, 545 105, 595 175" fill="none" stroke="#2563eb" stroke-width="2.2" marker-end="url(#fsm-arrow-blue)" />
  <g transform="translate(430, 80)">
    <rect x="0" y="0" width="165" height="42" rx="4" fill="#ffffff" stroke="#93c5fd" stroke-width="1.2" filter="url(#shadow)" />
    <text x="82" y="17" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#1d4ed8">write_buf not empty</text>
    <text x="82" y="32" text-anchor="middle" font-size="9.5" fill="#2563eb">Send DATA(seq); set t_send</text>
  </g>

  <!-- State 1: WAITING_FOR_ACK -->
  <g transform="translate(600, 150)">
    <rect x="0" y="0" width="240" height="135" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="2" filter="url(#shadow)" />
    <rect x="0" y="0" width="240" height="34" rx="8" fill="#d97706" />
    <text x="120" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#ffffff">WAITING_FOR_ACK (1)</text>
    <text x="15" y="56" font-size="10.5" fill="#1e293b">• Unacknowledged DATA in flight</text>
    <text x="15" y="75" font-size="10.5" fill="#1e293b">• Timeout timer active (t_send)</text>
    <text x="15" y="94" font-size="10.5" fill="#1e293b">• Awaiting peer positive ACK</text>
    <text x="15" y="112" font-size="10.5" fill="#1e293b">• Additional sends queued in buffer</text>
  </g>

  <!-- Lower Transition Path: Valid ACK Received (Curved downwards) -->
  <path d="M 600 265 C 545 335, 475 335, 425 265" fill="none" stroke="#16a34a" stroke-width="2.2" marker-end="url(#fsm-arrow-green)" />
  <g transform="translate(425, 315)">
    <rect x="0" y="0" width="175" height="42" rx="4" fill="#ffffff" stroke="#86efac" stroke-width="1.2" filter="url(#shadow)" />
    <text x="87" y="17" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#15803d">Valid ACK Arrives (A = S + 1)</text>
    <text x="87" y="32" text-anchor="middle" font-size="9.5" fill="#16a34a">dequeue(write_buf); S = (S+1)%256</text>
  </g>

  <!-- Self-loop on WAITING_FOR_ACK: Timeout retransmission (Wide loop encircling badge) -->
  <path d="M 840 195 C 970 140, 970 290, 840 235" fill="none" stroke="#dc2626" stroke-width="2.2" marker-end="url(#fsm-arrow-red)" />
  <g transform="translate(855, 185)">
    <rect x="0" y="0" width="85" height="58" rx="4" fill="#fef2f2" stroke="#dc2626" stroke-width="1.2" filter="url(#shadow)" />
    <text x="42" y="16" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#991b1b">TIMEOUT!</text>
    <text x="42" y="30" text-anchor="middle" font-size="8.5" fill="#dc2626">(now - t) &gt; T</text>
    <text x="42" y="44" text-anchor="middle" font-size="8" fill="#475569">Retransmit</text>
    <text x="42" y="53" text-anchor="middle" font-size="8" fill="#475569">reset timer</text>
  </g>

  <!-- Termination / k_close (Badge positioned to the side of vertical line) -->
  <line x1="310" y1="285" x2="310" y2="385" stroke="#64748b" stroke-width="1.8" stroke-dasharray="4 3" marker-end="url(#fsm-arrow)" />
  <rect x="225" y="325" width="72" height="22" rx="3" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" />
  <text x="261" y="340" text-anchor="middle" font-size="10" font-weight="bold" fill="#475569">k_close()</text>

  <g transform="translate(250, 395)">
    <circle cx="60" cy="20" r="16" fill="#ffffff" stroke="#1e293b" stroke-width="2" />
    <circle cx="60" cy="20" r="10" fill="#1e293b" />
    <text x="60" y="52" text-anchor="middle" font-size="11" font-weight="bold" fill="#475569">CLOSED</text>
  </g>
</svg>'''
    with open('figures/figure3_state_machine.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Generated figure3_state_machine.svg")


# ----------------------------------------------------------------------
# FIGURE 4A: Normal In-Order Transmission Sequence (SVG)
# ----------------------------------------------------------------------
def generate_figure4a():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 680" width="100%" height="100%" style="font-family: Arial, sans-serif; background-color: #ffffff;">
  <defs>
    <marker id="arr-black" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b" />
    </marker>
    <marker id="arr-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
    </marker>
    <marker id="arr-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
    </marker>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.08" />
    </filter>
  </defs>

  <text x="520" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">Figure 4A: Scenario 1 - Normal In-Order Transmission and Positive Acknowledgment</text>

  <!-- Host Enclosures -->
  <rect x="70" y="55" width="410" height="550" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4 3" />
  <text x="85" y="75" font-size="11" font-weight="bold" fill="#64748b">HOST A: SENDER NODE (127.0.0.1:5000)</text>

  <rect x="560" y="55" width="410" height="550" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4 3" />
  <text x="575" y="75" font-size="11" font-weight="bold" fill="#64748b">HOST B: RECEIVER NODE (127.0.0.1:5001)</text>

  <!-- Network Boundary Divider -->
  <line x1="520" y1="55" x2="520" y2="605" stroke="#e2e8f0" stroke-width="1.5" stroke-dasharray="2 4" />
  <text x="520" y="75" text-anchor="middle" font-size="10" font-weight="bold" fill="#94a3b8">UDP LINK</text>

  <!-- Lifeline Headers -->
  <rect x="90" y="90" width="120" height="36" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow)" />
  <text x="150" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#1d4ed8">user1.c</text>
  <text x="150" y="120" text-anchor="middle" font-size="9" fill="#3b82f6">Application</text>
  <line x1="150" y1="126" x2="150" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <rect x="300" y="90" width="135" height="36" rx="5" fill="#f1f5f9" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow)" />
  <text x="367" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0369a1">Sender Daemon</text>
  <text x="367" y="120" text-anchor="middle" font-size="9" fill="#0284c7">ktp_main (S &amp; R)</text>
  <line x1="367" y1="126" x2="367" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <rect x="605" y="90" width="135" height="36" rx="5" fill="#f1f5f9" stroke="#7c3aed" stroke-width="1.5" filter="url(#shadow)" />
  <text x="672" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#6d28d9">Receiver Daemon</text>
  <text x="672" y="120" text-anchor="middle" font-size="9" fill="#7c3aed">ktp_main (Thread R)</text>
  <line x1="672" y1="126" x2="672" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <rect x="830" y="90" width="120" height="36" rx="5" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5" filter="url(#shadow)" />
  <text x="890" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#15803d">user2.c</text>
  <text x="890" y="120" text-anchor="middle" font-size="9" fill="#22c55e">Application</text>
  <line x1="890" y1="126" x2="890" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <!-- Activation Bars -->
  <rect x="360" y="145" width="14" height="265" rx="2" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" />
  <rect x="665" y="270" width="14" height="75" rx="2" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5" />
  <rect x="665" y="475" width="14" height="50" rx="2" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5" />

  <!-- STEP 1 (t0): k_sendto (Local IPC) -->
  <line x1="150" y1="145" x2="358" y2="145" stroke="#1e293b" stroke-width="1.8" marker-end="url(#arr-black)" />
  <rect x="180" y="130" width="145" height="20" rx="3" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
  <text x="252" y="144" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#1e293b">k_sendto(fd, buf, 512)</text>

  <rect x="200" y="156" width="120" height="24" rx="3" fill="#fef3c7" stroke="#d97706" stroke-width="1" />
  <text x="260" y="172" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#92400e">Enqueued write_buf (1/10)</text>

  <!-- STEP 2 (t1 -> t2): UDP DATA transmission -->
  <line x1="374" y1="205" x2="663" y2="270" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arr-blue)" />
  
  <g transform="translate(440, 215)">
    <rect x="0" y="0" width="160" height="30" rx="4" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow)" />
    <rect x="0" y="0" width="38" height="30" rx="4" fill="#0284c7" />
    <text x="19" y="18" text-anchor="middle" font-size="10" font-weight="bold" fill="#ffffff">DATA</text>
    <text x="45" y="13" font-size="9" font-weight="bold" fill="#0f172a">Seq=1, Ack=1</text>
    <text x="45" y="24" font-size="8" fill="#64748b">512 Bytes Payload</text>
  </g>

  <!-- Sender Timer Bracket (t1 to t4) -->
  <line x1="280" y1="205" x2="280" y2="405" stroke="#d97706" stroke-width="2.5" />
  <polyline points="274,205 286,205" stroke="#d97706" stroke-width="2" />
  <polyline points="274,405 286,405" stroke="#d97706" stroke-width="2" />
  <text x="272" y="310" text-anchor="middle" font-size="9" font-weight="bold" fill="#b45309" transform="rotate(-90 272 310)">Timer (T=2s)</text>

  <!-- Receiver Note -->
  <g transform="translate(690, 260)">
    <rect x="0" y="0" width="165" height="42" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.2" filter="url(#shadow)" />
    <text x="8" y="14" font-size="8.5" font-weight="bold" fill="#166534">dropMessage(p) = 0 (Accepted)</text>
    <text x="8" y="26" font-size="8" fill="#15803d">• Seq 1 matches expected ack_no</text>
    <text x="8" y="37" font-size="8" fill="#15803d">• Enqueued to read_buf; ack_no = 2</text>
  </g>

  <!-- STEP 3 (t3 -> t4): UDP ACK transmission -->
  <line x1="665" y1="340" x2="376" y2="405" stroke="#16a34a" stroke-width="2.2" marker-end="url(#arr-green)" />

  <g transform="translate(440, 355)">
    <rect x="0" y="0" width="155" height="26" rx="4" fill="#ffffff" stroke="#16a34a" stroke-width="1.5" filter="url(#shadow)" />
    <rect x="0" y="0" width="34" height="26" rx="4" fill="#16a34a" />
    <text x="17" y="16" text-anchor="middle" font-size="10" font-weight="bold" fill="#ffffff">ACK</text>
    <text x="42" y="12" font-size="9" font-weight="bold" fill="#0f172a">Seq=1, Ack=2</text>
    <text x="42" y="22" font-size="8" fill="#166534">Cumulative Ack for Msg 1</text>
  </g>

  <!-- Sender Processing ACK -->
  <g transform="translate(185, 395)">
    <rect x="0" y="0" width="160" height="42" rx="4" fill="#eff6ff" stroke="#2563eb" stroke-width="1.2" filter="url(#shadow)" />
    <text x="8" y="14" font-size="8.5" font-weight="bold" fill="#1e40af">ACK Validated (Ack=2)</text>
    <text x="8" y="26" font-size="8" fill="#1d4ed8">• dequeue(write_buf)</text>
    <text x="8" y="37" font-size="8" fill="#1d4ed8">• State -&gt; WAITING_FOR_DATA</text>
  </g>

  <!-- STEP 4 (t5): k_recvfrom Request (Local IPC) -->
  <line x1="890" y1="480" x2="681" y2="480" stroke="#1e293b" stroke-width="1.8" marker-end="url(#arr-black)" />
  <rect x="715" y="465" width="130" height="19" rx="3" fill="#ffffff" stroke="#94a3b8" stroke-width="1" />
  <text x="780" y="478" text-anchor="middle" font-size="9" font-weight="bold" fill="#1e293b">k_recvfrom(fd, buf, 512)</text>

  <!-- STEP 5 (t6): k_recvfrom Return (Local IPC) -->
  <line x1="681" y1="520" x2="888" y2="520" stroke="#16a34a" stroke-width="1.8" marker-end="url(#arr-green)" />
  <rect x="710" y="505" width="145" height="28" rx="3" fill="#ffffff" stroke="#16a34a" stroke-width="1" filter="url(#shadow)" />
  <text x="782" y="518" text-anchor="middle" font-size="9" font-weight="bold" fill="#15803d">Returns 512 Bytes Payload</text>
  <text x="782" y="528" text-anchor="middle" font-size="7.5" fill="#166534">dequeue(read_buf); Memory freed</text>

  <!-- Bottom Execution Status -->
  <rect x="70" y="620" width="900" height="32" rx="5" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.2" />
  <text x="520" y="640" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#334155">Execution Summary: In-order delivery succeeded on 1st attempt (0 retransmissions, ratio = 1.0, latency = 1 RTT)</text>
</svg>'''
    with open('figures/figure4a_normal_transmission.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Generated figure4a_normal_transmission.svg")


# ----------------------------------------------------------------------
# FIGURE 4B: Packet Loss & Timeout Retransmission (SVG)
# ----------------------------------------------------------------------
def generate_figure4b():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 680" width="100%" height="100%" style="font-family: Arial, sans-serif; background-color: #ffffff;">
  <defs>
    <marker id="arr-black" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b" />
    </marker>
    <marker id="arr-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
    </marker>
    <marker id="arr-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
    </marker>
    <marker id="arr-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626" />
    </marker>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.08" />
    </filter>
  </defs>

  <text x="520" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">Figure 4B: Scenario 2 - Packet Loss and Timeout-Driven Retransmission (ARQ Recovery)</text>

  <!-- Host Enclosures -->
  <rect x="70" y="55" width="410" height="550" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4 3" />
  <text x="85" y="75" font-size="11" font-weight="bold" fill="#64748b">HOST A: SENDER NODE (127.0.0.1:5000)</text>

  <rect x="560" y="55" width="410" height="550" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4 3" />
  <text x="575" y="75" font-size="11" font-weight="bold" fill="#64748b">HOST B: RECEIVER NODE (127.0.0.1:5001)</text>

  <!-- Network Boundary Divider -->
  <line x1="520" y1="55" x2="520" y2="605" stroke="#e2e8f0" stroke-width="1.5" stroke-dasharray="2 4" />
  <text x="520" y="75" text-anchor="middle" font-size="10" font-weight="bold" fill="#94a3b8">UDP LINK</text>

  <!-- Lifeline Headers -->
  <rect x="90" y="90" width="120" height="36" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow)" />
  <text x="150" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#1d4ed8">user1.c</text>
  <text x="150" y="120" text-anchor="middle" font-size="9" fill="#3b82f6">Application</text>
  <line x1="150" y1="126" x2="150" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <rect x="300" y="90" width="135" height="36" rx="5" fill="#f1f5f9" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow)" />
  <text x="367" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0369a1">Sender Daemon</text>
  <text x="367" y="120" text-anchor="middle" font-size="9" fill="#0284c7">ktp_main (S &amp; R)</text>
  <line x1="367" y1="126" x2="367" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <rect x="605" y="90" width="135" height="36" rx="5" fill="#f1f5f9" stroke="#7c3aed" stroke-width="1.5" filter="url(#shadow)" />
  <text x="672" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#6d28d9">Receiver Daemon</text>
  <text x="672" y="120" text-anchor="middle" font-size="9" fill="#7c3aed">ktp_main (Thread R)</text>
  <line x1="672" y1="126" x2="672" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <rect x="830" y="90" width="120" height="36" rx="5" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5" filter="url(#shadow)" />
  <text x="890" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#15803d">user2.c</text>
  <text x="890" y="120" text-anchor="middle" font-size="9" fill="#22c55e">Application</text>
  <line x1="890" y1="126" x2="890" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <!-- Activation Bars -->
  <rect x="360" y="145" width="14" height="425" rx="2" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" />
  <rect x="665" y="435" width="14" height="75" rx="2" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5" />

  <!-- STEP 1 (t0): k_sendto (Local IPC) -->
  <line x1="150" y1="145" x2="358" y2="145" stroke="#1e293b" stroke-width="1.8" marker-end="url(#arr-black)" />
  <text x="254" y="138" text-anchor="middle" font-size="9" font-weight="bold" fill="#1e293b">k_sendto(fd, buf, 512)</text>

  <!-- STEP 2 (t1): Initial UDP Transmission (LOST IN TRANSIT) -->
  <line x1="374" y1="190" x2="505" y2="223" stroke="#0284c7" stroke-width="2.2" />
  <circle cx="520" cy="227" r="14" fill="#fee2e2" stroke="#dc2626" stroke-width="1.8" filter="url(#shadow)" />
  <line x1="513" y1="220" x2="527" y2="234" stroke="#dc2626" stroke-width="2.2" />
  <line x1="527" y1="220" x2="513" y2="234" stroke="#dc2626" stroke-width="2.2" />

  <!-- Loss Callout Badge (Positioned cleanly with clear margin, no line intersecting) -->
  <g transform="translate(542, 214)">
    <rect x="0" y="0" width="170" height="26" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.2" />
    <text x="10" y="13" font-size="8.5" font-weight="bold" fill="#991b1b">DROP: dropMessage(p) = 1</text>
    <text x="10" y="23" font-size="7.5" fill="#b91c1c">Packet lost; receiver gets nothing</text>
  </g>

  <!-- Initial DATA Packet Tag -->
  <rect x="390" y="175" width="105" height="18" rx="3" fill="#ffffff" stroke="#0284c7" stroke-width="1" />
  <text x="442" y="187" text-anchor="middle" font-size="8" font-weight="bold" fill="#0284c7">DATA [Seq=1, Len=512]</text>

  <!-- TIMER BRACKET (t1 to t_tout) - Generously placed in left gap -->
  <line x1="270" y1="190" x2="270" y2="335" stroke="#dc2626" stroke-width="2.5" />
  <polyline points="264,190 276,190" stroke="#dc2626" stroke-width="2" />
  <polyline points="264,335 276,335" stroke="#dc2626" stroke-width="2" />
  <text x="262" y="265" text-anchor="middle" font-size="9" font-weight="bold" fill="#b91c1c" transform="rotate(-90 262 265)">Countdown (T = 2.0s)</text>

  <!-- TIMEOUT ALERT BOX (Completely clear of lifeline at x=367) -->
  <g transform="translate(140, 315)">
    <rect x="0" y="0" width="115" height="44" rx="4" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5" filter="url(#shadow)" />
    <text x="57" y="15" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#991b1b">TIMEOUT EXPIRED</text>
    <text x="57" y="28" text-anchor="middle" font-size="7.5" fill="#b91c1c">(now - t_send) &gt; T</text>
    <text x="57" y="39" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#dc2626">Trigger Retransmit</text>
  </g>

  <!-- STEP 3 (t2 -> t3): Retransmission (Successful) -->
  <line x1="374" y1="375" x2="663" y2="435" stroke="#dc2626" stroke-width="2.4" marker-end="url(#arr-red)" />

  <!-- Retransmit Packet Badge -->
  <g transform="translate(440, 385)">
    <rect x="0" y="0" width="180" height="30" rx="4" fill="#ffffff" stroke="#dc2626" stroke-width="1.5" filter="url(#shadow)" />
    <rect x="0" y="0" width="45" height="30" rx="4" fill="#dc2626" />
    <text x="22" y="18" text-anchor="middle" font-size="9.5" font-weight="bold" fill="#ffffff">RETRY</text>
    <text x="52" y="13" font-size="9" font-weight="bold" fill="#0f172a">DATA Seq=1, Len=512</text>
    <text x="52" y="24" font-size="8" fill="#dc2626">send_time updated to t2</text>
  </g>

  <!-- Receiver Acceptance Note -->
  <g transform="translate(690, 425)">
    <rect x="0" y="0" width="165" height="42" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.2" filter="url(#shadow)" />
    <text x="8" y="14" font-size="8.5" font-weight="bold" fill="#166534">dropMessage(p) = 0 (Delivered)</text>
    <text x="8" y="26" font-size="8" fill="#15803d">• Packet recovered; into read_buf</text>
    <text x="8" y="37" font-size="8" fill="#15803d">• Expected ack_no advanced to 2</text>
  </g>

  <!-- STEP 4 (t3 -> t4): Returning ACK (Successful) -->
  <line x1="665" y1="505" x2="376" y2="570" stroke="#16a34a" stroke-width="2.2" marker-end="url(#arr-green)" />

  <!-- ACK Packet Badge -->
  <g transform="translate(450, 520)">
    <rect x="0" y="0" width="150" height="26" rx="4" fill="#ffffff" stroke="#16a34a" stroke-width="1.5" filter="url(#shadow)" />
    <rect x="0" y="0" width="34" height="26" rx="4" fill="#16a34a" />
    <text x="17" y="16" text-anchor="middle" font-size="10" font-weight="bold" fill="#ffffff">ACK</text>
    <text x="42" y="12" font-size="9" font-weight="bold" fill="#0f172a">Seq=1, Ack=2</text>
    <text x="42" y="22" font-size="8" fill="#166534">Confirms packet receipt</text>
  </g>

  <!-- Bottom Execution Status -->
  <rect x="70" y="620" width="900" height="32" rx="5" fill="#fef2f2" stroke="#ef4444" stroke-width="1.2" />
  <text x="520" y="640" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#991b1b">ARQ Recovery Summary: Forward packet drop recovered after T=2s timeout. Total transmissions = 2 (#Tx / #Msg = 2.0)</text>
</svg>'''
    with open('figures/figure4b_packet_loss.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Generated figure4b_packet_loss.svg")


# ----------------------------------------------------------------------
# FIGURE 4C: Lost Acknowledgment & Deduplication (SVG)
# ----------------------------------------------------------------------
def generate_figure4c():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 680" width="100%" height="100%" style="font-family: Arial, sans-serif; background-color: #ffffff;">
  <defs>
    <marker id="arr-black" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b" />
    </marker>
    <marker id="arr-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284c7" />
    </marker>
    <marker id="arr-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
    </marker>
    <marker id="arr-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626" />
    </marker>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1.5" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.08" />
    </filter>
  </defs>

  <text x="520" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#0f172a">Figure 4C: Scenario 3 - Lost Acknowledgment and Duplicate Packet Handling (Deduplication)</text>

  <!-- Host Enclosures -->
  <rect x="70" y="55" width="410" height="550" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4 3" />
  <text x="85" y="75" font-size="11" font-weight="bold" fill="#64748b">HOST A: SENDER NODE (127.0.0.1:5000)</text>

  <rect x="560" y="55" width="410" height="550" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="4 3" />
  <text x="575" y="75" font-size="11" font-weight="bold" fill="#64748b">HOST B: RECEIVER NODE (127.0.0.1:5001)</text>

  <!-- Network Boundary Divider -->
  <line x1="520" y1="55" x2="520" y2="605" stroke="#e2e8f0" stroke-width="1.5" stroke-dasharray="2 4" />
  <text x="520" y="75" text-anchor="middle" font-size="10" font-weight="bold" fill="#94a3b8">UDP LINK</text>

  <!-- Lifeline Headers -->
  <rect x="90" y="90" width="120" height="36" rx="5" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" filter="url(#shadow)" />
  <text x="150" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#1d4ed8">user1.c</text>
  <text x="150" y="120" text-anchor="middle" font-size="9" fill="#3b82f6">Application</text>
  <line x1="150" y1="126" x2="150" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <rect x="300" y="90" width="135" height="36" rx="5" fill="#f1f5f9" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow)" />
  <text x="367" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#0369a1">Sender Daemon</text>
  <text x="367" y="120" text-anchor="middle" font-size="9" fill="#0284c7">ktp_main (S &amp; R)</text>
  <line x1="367" y1="126" x2="367" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <rect x="605" y="90" width="135" height="36" rx="5" fill="#f1f5f9" stroke="#7c3aed" stroke-width="1.5" filter="url(#shadow)" />
  <text x="672" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#6d28d9">Receiver Daemon</text>
  <text x="672" y="120" text-anchor="middle" font-size="9" fill="#7c3aed">ktp_main (Thread R)</text>
  <line x1="672" y1="126" x2="672" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <rect x="830" y="90" width="120" height="36" rx="5" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5" filter="url(#shadow)" />
  <text x="890" y="108" text-anchor="middle" font-size="11.5" font-weight="bold" fill="#15803d">user2.c</text>
  <text x="890" y="120" text-anchor="middle" font-size="9" fill="#22c55e">Application</text>
  <line x1="890" y1="126" x2="890" y2="590" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="4 4" />

  <!-- Activation Bars -->
  <rect x="360" y="145" width="14" height="425" rx="2" fill="#e0f2fe" stroke="#0284c7" stroke-width="1.5" />
  <rect x="665" y="200" width="14" height="60" rx="2" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5" />
  <rect x="665" y="415" width="14" height="85" rx="2" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5" />

  <!-- STEP 1 (t0 -> t1): Initial DATA transmission (Delivered) -->
  <line x1="374" y1="150" x2="663" y2="205" stroke="#0284c7" stroke-width="2.2" marker-end="url(#arr-blue)" />
  
  <g transform="translate(440, 160)">
    <rect x="0" y="0" width="150" height="24" rx="3" fill="#ffffff" stroke="#0284c7" stroke-width="1" />
    <text x="75" y="16" text-anchor="middle" font-size="9" font-weight="bold" fill="#0284c7">DATA [Seq=1, "hello"]</text>
  </g>

  <!-- Receiver First Arrival Note (Placed in right gap, clear of user2 lifeline) -->
  <g transform="translate(690, 195)">
    <rect x="0" y="0" width="135" height="38" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.2" filter="url(#shadow)" />
    <text x="8" y="14" font-size="8.5" font-weight="bold" fill="#166534">Stored in read_buf</text>
    <text x="8" y="26" font-size="8" fill="#15803d">Expected ack_no = 2</text>
  </g>

  <!-- STEP 2 (t1 -> t_acklost): Returning ACK Transmitted (DROPPED!) -->
  <line x1="665" y1="245" x2="535" y2="272" stroke="#16a34a" stroke-width="2.2" />
  <circle cx="520" cy="275" r="14" fill="#fee2e2" stroke="#dc2626" stroke-width="1.8" filter="url(#shadow)" />
  <line x1="513" y1="268" x2="527" y2="282" stroke="#dc2626" stroke-width="2.2" />
  <line x1="527" y1="268" x2="513" y2="282" stroke="#dc2626" stroke-width="2.2" />

  <!-- Loss Callout Badge (Positioned cleanly above drop point, zero intersecting lines) -->
  <g transform="translate(425, 230)">
    <rect x="0" y="0" width="190" height="26" rx="4" fill="#fee2e2" stroke="#dc2626" stroke-width="1.2" />
    <text x="95" y="12" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#991b1b">ACK DROPPED IN TRANSIT</text>
    <text x="95" y="22" text-anchor="middle" font-size="7.5" fill="#b91c1c">dropMessage(p) = 1; Sender lost ACK</text>
  </g>

  <!-- Timer Bracket on Sender -->
  <line x1="270" y1="150" x2="270" y2="325" stroke="#dc2626" stroke-width="2.5" />
  <polyline points="264,150 276,150" stroke="#dc2626" stroke-width="2" />
  <polyline points="264,325 276,325" stroke="#dc2626" stroke-width="2" />
  <text x="262" y="240" text-anchor="middle" font-size="9" font-weight="bold" fill="#b91c1c" transform="rotate(-90 262 240)">Countdown (T = 2.0s)</text>

  <!-- Timeout Box in left gap -->
  <g transform="translate(140, 305)">
    <rect x="0" y="0" width="115" height="42" rx="4" fill="#fef2f2" stroke="#dc2626" stroke-width="1.5" filter="url(#shadow)" />
    <text x="57" y="15" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#991b1b">TIMEOUT EXPIRED</text>
    <text x="57" y="28" text-anchor="middle" font-size="7.5" fill="#b91c1c">Retransmitting</text>
    <text x="57" y="38" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#dc2626">DATA [Seq=1]</text>
  </g>

  <!-- STEP 3 (t2): Sender Retransmits Duplicate DATA -->
  <line x1="374" y1="360" x2="663" y2="420" stroke="#dc2626" stroke-width="2.4" marker-end="url(#arr-red)" />
  
  <g transform="translate(440, 370)">
    <rect x="0" y="0" width="165" height="28" rx="4" fill="#ffffff" stroke="#dc2626" stroke-width="1.5" filter="url(#shadow)" />
    <rect x="0" y="0" width="55" height="28" rx="4" fill="#dc2626" />
    <text x="27" y="17" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">RETRY</text>
    <text x="62" y="12" font-size="8.5" font-weight="bold" fill="#0f172a">DATA Seq=1</text>
    <text x="62" y="22" font-size="7.5" fill="#dc2626">Duplicate frame</text>
  </g>

  <!-- DEDUPLICATION LOGIC CALLOUT (Placed cleanly in right gap without crossing lifeline 890) -->
  <g transform="translate(690, 405)">
    <rect x="0" y="0" width="135" height="56" rx="4" fill="#fefce8" stroke="#ca8a04" stroke-width="1.5" filter="url(#shadow)" />
    <text x="8" y="14" font-size="8.5" font-weight="bold" fill="#854d0e">DUPLICATE DETECTED</text>
    <text x="8" y="26" font-size="7.5" fill="#a16207">Seq (1) &lt; Expected (2)</text>
    <text x="8" y="38" font-size="7.5" font-weight="bold" fill="#dc2626">• Discard payload</text>
    <text x="8" y="50" font-size="7.5" font-weight="bold" fill="#15803d">• Re-send ACK(2)</text>
  </g>

  <!-- STEP 4 (t3): Receiver Re-sends Cumulative ACK (Success) -->
  <line x1="665" y1="490" x2="376" y2="550" stroke="#16a34a" stroke-width="2.4" marker-end="url(#arr-green)" />

  <g transform="translate(445, 505)">
    <rect x="0" y="0" width="165" height="28" rx="4" fill="#ffffff" stroke="#16a34a" stroke-width="1.5" filter="url(#shadow)" />
    <rect x="0" y="0" width="48" height="28" rx="4" fill="#16a34a" />
    <text x="24" y="17" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">RE-ACK</text>
    <text x="54" y="12" font-size="9" font-weight="bold" fill="#0f172a">ACK Seq=1, Ack=2</text>
    <text x="54" y="22" font-size="8" fill="#166534">Clears sender buffer</text>
  </g>

  <!-- Sender Unlocked Note -->
  <g transform="translate(140, 530)">
    <rect x="0" y="0" width="115" height="38" rx="4" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.2" filter="url(#shadow)" />
    <text x="57" y="15" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#166534">write_buf Dequeued</text>
    <text x="57" y="28" text-anchor="middle" font-size="7.5" fill="#15803d">Socket unlocked</text>
  </g>

  <!-- Bottom Execution Status -->
  <rect x="70" y="620" width="900" height="32" rx="5" fill="#fefce8" stroke="#ca8a04" stroke-width="1.2" />
  <text x="520" y="640" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#854d0e">Deduplication Invariant Guaranteed: Receiver stores exactly 1 payload; cumulative ACK unlocks sender without buffer corruption</text>
</svg>'''
    with open('figures/figure4c_lost_ack.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Generated figure4c_lost_ack.svg")


# ----------------------------------------------------------------------
# FIGURE 5: Circular Queue & Buffer Architecture (SVG)
# ----------------------------------------------------------------------
def generate_figure5():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 560" width="100%" height="100%" style="font-family: Arial, sans-serif; background-color: #ffffff;">
  <defs>
    <marker id="buf-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b" />
    </marker>
    <marker id="buf-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a" />
    </marker>
    <marker id="buf-orange" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#d97706" />
    </marker>
  </defs>

  <text x="480" y="32" text-anchor="middle" font-size="17" font-weight="bold" fill="#1e293b">Figure 5: Circular FIFO Buffer Architecture (struct queue in queue.h)</text>

  <!-- Top container: Slot Layout -->
  <g transform="translate(80, 60)">
    <text x="0" y="0" font-size="13" font-weight="bold" fill="#334155">A. Circular Queue Memory Layout (BUF_SIZE = 10, Slot Payload = 512 Bytes)</text>

    <!-- Pointer label for FRONT (pointing down from above) -->
    <line x1="200" y1="18" x2="200" y2="40" stroke="#16a34a" stroke-width="2.2" marker-end="url(#buf-green)" />
    <rect x="145" y="0" width="110" height="20" rx="3" fill="#f0fdf4" stroke="#16a34a" stroke-width="1" />
    <text x="200" y="14" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#166534">front = 2 (Dequeue)</text>

    <!-- Pointer label for BACK (pointing up from below) -->
    <line x1="440" y1="145" x2="440" y2="120" stroke="#d97706" stroke-width="2.2" marker-end="url(#buf-orange)" />
    <rect x="385" y="148" width="110" height="20" rx="3" fill="#fffbeb" stroke="#d97706" stroke-width="1" />
    <text x="440" y="162" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#92400e">back = 5 (Enqueue)</text>

    <!-- Slots 0 through 9 -->
    <!-- Slot 0 -->
    <rect x="0" y="45" width="76" height="70" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5" />
    <text x="38" y="70" text-anchor="middle" font-size="11" font-weight="bold" fill="#64748b">Slot 0</text>
    <text x="38" y="92" text-anchor="middle" font-size="10" fill="#94a3b8">Empty</text>

    <!-- Slot 1 -->
    <rect x="80" y="45" width="76" height="70" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5" />
    <text x="118" y="70" text-anchor="middle" font-size="11" font-weight="bold" fill="#64748b">Slot 1</text>
    <text x="118" y="92" text-anchor="middle" font-size="10" fill="#94a3b8">Empty</text>

    <!-- Slot 2 (Front) -->
    <rect x="160" y="45" width="76" height="70" fill="#dbeafe" stroke="#2563eb" stroke-width="2" />
    <text x="198" y="68" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">Slot 2</text>
    <text x="198" y="86" text-anchor="middle" font-size="10" font-weight="bold" fill="#2563eb">Msg #1</text>
    <text x="198" y="102" text-anchor="middle" font-size="8.5" fill="#1d4ed8">512 Bytes</text>

    <!-- Slot 3 -->
    <rect x="240" y="45" width="76" height="70" fill="#dbeafe" stroke="#2563eb" stroke-width="2" />
    <text x="278" y="68" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">Slot 3</text>
    <text x="278" y="86" text-anchor="middle" font-size="10" font-weight="bold" fill="#2563eb">Msg #2</text>
    <text x="278" y="102" text-anchor="middle" font-size="8.5" fill="#1d4ed8">512 Bytes</text>

    <!-- Slot 4 -->
    <rect x="320" y="45" width="76" height="70" fill="#dbeafe" stroke="#2563eb" stroke-width="2" />
    <text x="358" y="68" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">Slot 4</text>
    <text x="358" y="86" text-anchor="middle" font-size="10" font-weight="bold" fill="#2563eb">Msg #3</text>
    <text x="358" y="102" text-anchor="middle" font-size="8.5" fill="#1d4ed8">512 Bytes</text>

    <!-- Slot 5 (Back) -->
    <rect x="400" y="45" width="76" height="70" fill="#dbeafe" stroke="#2563eb" stroke-width="2" />
    <text x="438" y="68" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">Slot 5</text>
    <text x="438" y="86" text-anchor="middle" font-size="10" font-weight="bold" fill="#2563eb">Msg #4</text>
    <text x="438" y="102" text-anchor="middle" font-size="8.5" fill="#1d4ed8">512 Bytes</text>

    <!-- Slots 6 - 9 -->
    <rect x="480" y="45" width="76" height="70" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5" />
    <text x="518" y="70" text-anchor="middle" font-size="11" font-weight="bold" fill="#64748b">Slot 6</text>
    <text x="518" y="92" text-anchor="middle" font-size="10" fill="#94a3b8">Empty</text>

    <rect x="560" y="45" width="76" height="70" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5" />
    <text x="598" y="70" text-anchor="middle" font-size="11" font-weight="bold" fill="#64748b">Slot 7</text>
    <text x="598" y="92" text-anchor="middle" font-size="10" fill="#94a3b8">Empty</text>

    <rect x="640" y="45" width="76" height="70" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5" />
    <text x="678" y="70" text-anchor="middle" font-size="11" font-weight="bold" fill="#64748b">Slot 8</text>
    <text x="678" y="92" text-anchor="middle" font-size="10" fill="#94a3b8">Empty</text>

    <rect x="720" y="45" width="76" height="70" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5" />
    <text x="758" y="70" text-anchor="middle" font-size="11" font-weight="bold" fill="#64748b">Slot 9</text>
    <text x="758" y="92" text-anchor="middle" font-size="10" fill="#94a3b8">Empty</text>

    <!-- Circular wrap-around arrow (Deepened arc with >45px clearance below back=5 pointer) -->
    <path d="M 758 120 C 758 220, 38 220, 38 122" fill="none" stroke="#64748b" stroke-width="1.8" stroke-dasharray="4 3" marker-end="url(#buf-arrow)" />
    <rect x="310" y="210" width="180" height="20" rx="3" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" />
    <text x="400" y="224" text-anchor="middle" font-size="9" fill="#475569" font-weight="bold">Wrap-around: (index + 1) % 10</text>
  </g>

  <!-- Lower Container: Algebraic Queue Invariants -->
  <g transform="translate(80, 315)">
    <rect x="0" y="0" width="800" height="195" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" />
    <text x="25" y="28" font-size="13" font-weight="bold" fill="#1e293b">B. Queue State Definitions, Invariants, and Wrap-around Rules</text>

    <!-- Condition 1: Initialization -->
    <rect x="25" y="45" width="235" height="135" rx="6" fill="#ffffff" stroke="#e2e8f0" stroke-width="1" />
    <text x="142" y="68" text-anchor="middle" font-size="12" font-weight="bold" fill="#334155">Initialization: init_queue()</text>
    <text x="38" y="92" font-size="10.5" fill="#475569">• front = 0</text>
    <text x="38" y="110" font-size="10.5" fill="#475569">• back = BUF_SIZE - 1 (9)</text>
    <text x="38" y="128" font-size="10.5" fill="#475569">• memset(data, 0, sizeof)</text>
    <text x="38" y="152" font-size="10" fill="#16a34a" font-weight="bold">Empty State: 0 elements</text>
    <text x="38" y="167" font-size="9" fill="#64748b">Capacity: 10 × 512B slots</text>

    <!-- Condition 2: is_empty() -->
    <rect x="282" y="45" width="235" height="135" rx="6" fill="#ffffff" stroke="#e2e8f0" stroke-width="1" />
    <text x="400" y="68" text-anchor="middle" font-size="12" font-weight="bold" fill="#334155">Empty Check: is_empty()</text>
    <text x="295" y="92" font-size="10.5" fill="#475569">Formula:</text>
    <text x="295" y="112" font-size="10.5" font-weight="bold" fill="#2563eb">front == (back + 1) % BUF_SIZE</text>
    <text x="295" y="136" font-size="10" fill="#475569">Returns 1 if no elements</text>
    <text x="295" y="152" font-size="10" fill="#64748b">k_recvfrom() non-blocking</text>
    <text x="295" y="167" font-size="9" fill="#dc2626">Returns -1 with ENOMEM</text>

    <!-- Condition 3: is_full() -->
    <rect x="540" y="45" width="235" height="135" rx="6" fill="#ffffff" stroke="#e2e8f0" stroke-width="1" />
    <text x="657" y="68" text-anchor="middle" font-size="12" font-weight="bold" fill="#334155">Full Check: is_full()</text>
    <text x="555" y="92" font-size="10.5" fill="#475569">Formula:</text>
    <text x="555" y="112" font-size="10.5" font-weight="bold" fill="#dc2626">front == (back + 2) % BUF_SIZE</text>
    <text x="555" y="136" font-size="10" fill="#475569">Returns 1 if 9 slots occupied</text>
    <text x="555" y="152" font-size="10" fill="#64748b">k_sendto() flow control</text>
    <text x="555" y="167" font-size="9" fill="#dc2626">Returns -1 (Backpressure)</text>
  </g>
</svg>'''
    with open('figures/figure5_circular_buffer.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Generated figure5_circular_buffer.svg")


if __name__ == "__main__":
    generate_figure1()
    generate_figure3()
    generate_figure4a()
    generate_figure4b()
    generate_figure4c()
    generate_figure5()
    generate_figure6()
    print("All schematic figures and graphs generated successfully in 'figures/' directory.")

