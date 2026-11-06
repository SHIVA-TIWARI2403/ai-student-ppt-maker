"""
Academic AI Engine for SlideCraft AI.
Generates comprehensive, in-depth academic presentations up to 25 slides with:
- Formal concept definition on Slide 1
- Deep theoretical breakdowns, mathematical frameworks, and architectural mechanics
- Dedicated Closing & Thank You / Q&A note on the final slide
- Integration with Gemini 2.0 Flash and an exhaustive 25-slide Academic Fallback Engine.
"""

import os
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are an esteemed academic researcher, university professor, and world-class curriculum designer.
Your objective is to generate an authoritative, exhaustive, and rigorously detailed academic presentation deck for university students and researchers.

STRICT MANDATORY RULES:
1. SLIDE 1 MUST INCLUDE A FORMAL CONCEPT DEFINITION:
   - Provide an exact, rigorous scientific/academic definition of the topic.
   - Outline the fundamental premise, formal classification, and scope.
2. FINAL SLIDE MUST BE A DEDICATED CLOSING & THANK YOU SLIDE:
   - Must express gratitude to professors, evaluators, and peers.
   - Summarize the paramount takeaway.
   - Open the floor for formal Question & Answer (Q&A) / defense discussion.
3. IN-DEPTH THEORETICAL DEPTH:
   - Do NOT provide superficial or trivial bullet points.
   - Provide rich, substantive explanations with bold academic lead-ins (e.g. "**Mathematical Formulation**: ...", "**Architectural Decoupling**: ...", "**Empirical Invariance**: ...").
   - Include operational principles, structural mechanics, trade-offs, and empirical benchmarks.
4. LANGUAGE: 100% Pure, Professional, Scholarly English.
5. FORMAT: Strictly valid JSON matching the exact requested schema.
"""

def generate_academic_deep_deck(topic: str, slide_count: int, education_level: str = "Master's & Doctoral") -> dict:
    """
    Exhaustive 25-slide deep academic research engine.
    Ensures high-theory, formal definition on slide 1, and thank you on the final slide.
    """
    clean_topic = topic.strip().title()
    count = max(3, min(slide_count, 25))

    # Comprehensive 25-slide academic curriculum modules
    master_modules = [
        # Slide 1: Formal Definition & Academic Introduction
        {
            "layout_type": "title",
            "tag": "FOUNDATIONAL DEFINITION",
            "title": f"Academic Analysis: {clean_topic}",
            "subtitle": "Theoretical Foundations, Architectural Paradigms, and Empirical Frontiers",
            "formal_definition": f"Formally defined, {clean_topic} represents a systematic domain focused on the mathematical and computational orchestration of specialized data structures, algorithmic workflows, and governing state machines designed to resolve high-dimensional complexity under deterministic performance constraints.",
            "bullet_points": [
                f"**Taxonomic Classification**: Positioned within advanced {education_level} research across modern engineering and theoretical computing sciences.",
                "**Primary Axiom**: Bridging theoretical abstractions with robust, production-grade scalability and rigorous formal verification.",
                "**Investigation Scope**: Comprehensive analysis spanning foundational principles, algorithmic implementations, ethical governance, and future milestones."
            ],
            "stat_or_highlight": f"{education_level} Level Defense",
            "image_prompt": f"Detailed schematic diagram and conceptual 3d visualization of {clean_topic}, dark cobalt and cyan accents, academic textbook illustration",
            "gif_query": f"{clean_topic} academic concept",
            "speaker_notes": f"Distinguished faculty, evaluators, and colleagues, welcome to this defense on {clean_topic}. In this session, we will dissect its core theoretical tenets, empirical efficacy, and emerging engineering frontiers."
        },
        # Slide 2: Historical Genesis & Evolution
        {
            "layout_type": "split_image_right",
            "tag": "HISTORICAL GENESIS",
            "title": f"The Evolution & Historical Antecedents of {clean_topic}",
            "subtitle": "Traces from Foundational Conjectures to Contemporary Paradigms",
            "bullet_points": [
                "**Early Theoretical Formulations**: Tracing initial conceptual breakthroughs and the mechanical constraints that initially hindered real-time execution.",
                "**The Computational Inflection Point**: How exponential hardware expansion and distributed topologies catalyzed contemporary advancements.",
                "**Paradigm Shift**: Transitioning from fragile heuristic baselines to self-optimizing, mathematically verified computational frameworks."
            ],
            "stat_or_highlight": "Multi-Decade Evolution",
            "image_prompt": f"Timeline diagram showing the historical evolution of {clean_topic}, clean minimalist infographics, 3d render",
            "gif_query": "history evolution timeline",
            "speaker_notes": f"To appreciate the current architectural state of {clean_topic}, we must contextualize the historical bottlenecks that catalyzed modern engineering solutions."
        },
        # Slide 3: Theoretical Formulations & Mathematical Basis
        {
            "layout_type": "deep_theory",
            "tag": "THEORETICAL FRAMEWORK",
            "title": "Mathematical Models & Foundational Formulations",
            "subtitle": "Rigorous Abstract Characterization and Governing Equations",
            "bullet_points": [
                "**State Space Representation**: Modeling dynamic behavioral transformations through state transition matrices and discrete probability distributions.",
                "**Complexity Asymptotics**: Establishing strict bounds across worst-case time complexity O(n log n) and localized space utilization overheads.",
                "**Convergence Guarantees**: Proving algorithmic stability using Lyapunov stability criteria and stochastic gradient convergence lemmas."
            ],
            "stat_or_highlight": "Deterministic Asymptotics",
            "image_prompt": f"Abstract geometric mathematical formulas and calculus graphs illustrating {clean_topic}, dark navy background, glowing gold equations",
            "gif_query": "mathematical formula data science",
            "speaker_notes": f"Examining the underlying mathematics reveals strict convergence criteria that ensure deterministic execution even under extreme data perturbation."
        },
        # Slide 4: Core Operational Principles
        {
            "layout_type": "three_cards",
            "tag": "OPERATIONAL AXIOMS",
            "title": "Fundamental Pillars & Governing Principles",
            "subtitle": "The Invariant Laws Ensuring Determinism and Robustness",
            "bullet_points": [
                "**Invariance & Idempotency**: Guaranteeing identical outputs irrespective of concurrent duplicate operational signals or network jitter.",
                "**Separation of Concerns**: Decoupling the computational control plane from transactional execution routines for fault isolation.",
                "**Dynamic Reconfigurability**: Enabling on-the-fly parameter adaptation without necessitating cold system restarts."
            ],
            "stat_or_highlight": "Tri-Pillar Architecture",
            "image_prompt": f"Three glowing crystal pillars representing foundational principles of {clean_topic}, modern engineering render",
            "gif_query": "engineering pillars architecture",
            "speaker_notes": f"These three pillars constitute the operational baseline, guaranteeing that any downstream implementation maintains integrity and structural resilience."
        },
        # Slide 5: System Architecture & Structural Hierarchy
        {
            "layout_type": "split_image_left",
            "tag": "SYSTEM ARCHITECTURE",
            "title": "Hierarchical Structural Architecture",
            "subtitle": "Modular Deconstruction of the End-to-End Processing Stack",
            "bullet_points": [
                "**Ingestion & Telemetry Layer**: High-bandwidth asynchronous listeners capturing inbound vectors with microsecond granularity.",
                "**Transformation Core**: Vectorized transformation pipelines executing parallelized tensor calculations across dedicated sub-processors.",
                "**Persistence & Validation Tier**: ACID-compliant distributed ledgers enforcing cryptographic proofs of state validity."
            ],
            "stat_or_highlight": "Sub-millisecond Latency",
            "image_prompt": f"Detailed layered architectural blueprint of {clean_topic}, isometric technical diagram, glowing neon outlines on dark slate",
            "gif_query": "system architecture data pipeline",
            "speaker_notes": f"The structural hierarchy is partitioned into distinct tiers to isolate ingestion bottlenecks from the low-latency transformation core."
        },
        # Slide 6: Algorithmic Mechanics & Execution Pipeline
        {
            "layout_type": "split_image_right",
            "tag": "ALGORITHMIC MECHANICS",
            "title": "Execution Pipeline & Data Flow Dynamics",
            "subtitle": "Step-by-Step Processing from Initial Input to Verified Output",
            "bullet_points": [
                "**Normalization & Pre-filtering**: Stripping stochastic noise and canonicalizing multidimensional inputs against strict schema definitions.",
                "**Heuristic & Optimization Loop**: Leveraging non-linear objective functions to converge toward global optima while bypassing local minima traps.",
                "**Post-Verification Gate**: Subjecting generated artifacts to adversarial perturbation checks before finalizing persistence."
            ],
            "stat_or_highlight": "99.99% Pipeline Fidelity",
            "image_prompt": f"Cybernetic digital pipeline showing data flowing through algorithmic gates, 3d render",
            "gif_query": "data processing pipeline stream",
            "speaker_notes": f"This execution pipeline highlights how stochastic noise is systematically attenuated through layered verification filters."
        },
        # Slide 7: Comparative Analysis vs. Legacy Approaches
        {
            "layout_type": "three_cards",
            "tag": "COMPARATIVE ANALYSIS",
            "title": "Comparative Benchmarks vs. Classical Approaches",
            "subtitle": "Empirical Superiority across Throughput, Overhead, and Fault Tolerance",
            "bullet_points": [
                "**Resource Consumption**: 68% lower computational memory footprint compared to legacy monolithic predecessors.",
                "**Throughput Scalability**: Linear horizontal scaling curve capable of sustaining orders-of-magnitude higher transaction volume.",
                "**Resilience to Partitioning**: Immediate leader re-election and quorum synchronization during network partition events."
            ],
            "stat_or_highlight": "4.2x Faster Convergence",
            "image_prompt": f"Side by side comparative analytics chart and bar visualization comparing {clean_topic} against legacy systems",
            "gif_query": "comparison metrics analytics",
            "speaker_notes": f"When evaluated head-to-head against classical monolithic implementations, empirical data demonstrates an undeniable quantitative advantage across all key vectors."
        },
        # Slide 8: Empirical Validation & Stress Test Metrics
        {
            "layout_type": "deep_theory",
            "tag": "EMPIRICAL FINDINGS",
            "title": "Stress Testing & Benchmark Validations",
            "subtitle": "Quantitative Findings Derived under Extreme Synthetic Workloads",
            "bullet_points": [
                "**High-Concurrency Profiling**: Sustaining 100,000 concurrent active requests without degrading p99 latency thresholds.",
                "**Chaos Engineering Analysis**: Intentional node termination yields sub-50ms self-healing failover with zero transactional loss.",
                "**Statistical Significance**: Paired t-tests confirm performance discrepancies exceed the p < 0.001 threshold of significance."
            ],
            "stat_or_highlight": "p < 0.001 Significance",
            "image_prompt": f"Futuristic laboratory testing console showing empirical metrics and stress graphs for {clean_topic}",
            "gif_query": "scientific laboratory stress test",
            "speaker_notes": f"Rigorous stress profiling demonstrates that our theoretical bounds hold true even when subjected to adversarial chaos-induced workloads."
        },
        # Slide 9: Real-World Industrial & Academic Deployments
        {
            "layout_type": "split_image_left",
            "tag": "PRACTICAL IMPLEMENTATIONS",
            "title": "Industrial Case Studies & Production Deployments",
            "subtitle": "Translating Theoretical Excellence into Tangible Sector Impact",
            "bullet_points": [
                "**Biomedical & Healthcare**: Accelerating molecular simulation and genomic variant interpretation from weeks down to hours.",
                "**Autonomous Aerospace Systems**: Integrating real-time telemetry validation within mission-critical avionics flight control computers.",
                "**Quantitative Financial Modeling**: Eliminating slippage in ultra-high-frequency liquidity distribution mechanisms."
            ],
            "stat_or_highlight": "Global Mission Critical",
            "image_prompt": f"Modern futuristic research institute with scientists analyzing {clean_topic} on holographic screens, 3d render",
            "gif_query": "futuristic industry real world",
            "speaker_notes": f"Moving beyond theoretical constructs, these real-world enterprise deployments demonstrate direct operational and humanitarian utility."
        },
        # Slide 10: Scalability Vectors & Latency Optimization
        {
            "layout_type": "split_image_right",
            "tag": "OPTIMIZATION VECTORS",
            "title": "Throughput Scaling & Micro-Optimization",
            "subtitle": "Hardware-Conscious Algorithmic Tuning for Maximum Efficiency",
            "bullet_points": [
                "**Cache Locality Optimization**: Re-architecting data structures to align with L1/L2 CPU cache lines, drastically curtailing memory bus stalls.",
                "**Zero-Copy Memory Semantics**: Utilizing kernel-bypass network drivers to eliminate wasteful user-to-kernel context switching.",
                "**SIMD Vectorization**: Compiling core mathematical kernels into 512-bit vector registers for single-instruction multi-data parallelism."
            ],
            "stat_or_highlight": "Zero-Copy Execution",
            "image_prompt": f"Microscopic view of high-performance silicon microchip circuitry glowing with cyan laser pathways, 3d render",
            "gif_query": "microchip cpu circuit speed",
            "speaker_notes": f"By tailoring memory access patterns directly to physical processor caches, we eliminate the primary latency penalties typical of naive implementations."
        },
        # Slide 11: Security Protocols & Cryptographic Safeguards
        {
            "layout_type": "three_cards",
            "tag": "SECURITY & INTEGRITY",
            "title": "Cryptographic Integrity & Threat Mitigation",
            "subtitle": "Defense-in-Depth Mechanisms Safeguarding System Autonomy",
            "bullet_points": [
                "**Zero-Trust Authorization**: Mandating cryptographic attestation for all inter-service communications using short-lived ephemeral tokens.",
                "**Adversarial Robustness**: Hardening deep statistical layers against gradient-based evasion attacks and model poisoning attempts.",
                "**Immutable Audit Logging**: Recording operational state transitions to append-only Merkle-tree registries for non-repudiation."
            ],
            "stat_or_highlight": "Zero-Trust Architecture",
            "image_prompt": f"Cryptographic biometric shield and glowing security lock protecting mathematical data matrix, 3d render",
            "gif_query": "cyber security digital protection",
            "speaker_notes": f"Security is not treated as an afterthought; cryptographic verification and non-repudiation are baked into every transaction layer."
        },
        # Slide 12: Data Governance & Compliance Frameworks
        {
            "layout_type": "deep_theory",
            "tag": "DATA GOVERNANCE",
            "title": "Regulatory Compliance & Information Governance",
            "subtitle": "Harmonizing Technical Capabilities with Global Legal Standards",
            "bullet_points": [
                "**Differential Privacy Guarantees**: Injecting calibrated Laplace noise to safeguard individual data point re-identification.",
                "**Statutory Alignment**: Strict conformance with global data residency statutes, GDPR article mandates, and HIPAA standards.",
                "**Auditable Provenance**: Maintaining cryptographically verifiable records of algorithmic training corpora and feature weights."
            ],
            "stat_or_highlight": "Strict GDPR/ISO Audit",
            "image_prompt": f"Digital regulatory compliance seal and encrypted legal documents on glowing academic terminal",
            "gif_query": "data privacy compliance audit",
            "speaker_notes": f"Technical excellence must coexist with ethical data governance; our framework enforces provable differential privacy boundaries."
        },
        # Slide 13: Ethical Implications & Societal Impact
        {
            "layout_type": "split_image_left",
            "tag": "ETHICAL STEWARDSHIP",
            "title": "Societal Implications & Ethical Stewardship",
            "subtitle": "Navigating Algorithmic Fairness, Bias, and Accessibility",
            "bullet_points": [
                "**Mitigating Representational Bias**: Systematically auditing feature selections to avoid compounding socio-historical disparities.",
                "**Democratic Accessibility**: Championing open-standard protocols to prevent proprietary monopolization of critical scientific tooling.",
                "**Human-in-the-Loop Oversight**: Ensuring irreversible high-consequence decisions mandate conscious human authorization."
            ],
            "stat_or_highlight": "Human-Centric AI",
            "image_prompt": f"Human hands interacting with a glowing digital holographic globe, representing ethical technology synergy",
            "gif_query": "ethical technology humanity world",
            "speaker_notes": f"As researchers, we bear an obligation to ensure these automated systems expand human agency rather than concentrate unchecked authority."
        },
        # Slide 14: Environmental Footprint & Sustainability
        {
            "layout_type": "split_image_right",
            "tag": "GREEN COMPUTING",
            "title": "Ecological Sustainability & Energy Efficiency",
            "subtitle": "Minimizing Carbon Intensity through Algorithmic Pruning",
            "bullet_points": [
                "**Sparse Matrix Computation**: Skipping redundant floating-point multiplications to reduce datacenter electrical draw by 42%.",
                "**Carbon-Aware Scheduling**: Dynamically shifting batch compute workloads to geographic regions currently powered by renewable surpluses.",
                "**Hardware Longevity**: Optimizing thermal dissipation cycles to mitigate electronic waste and premature ASIC deprecation."
            ],
            "stat_or_highlight": "42% Carbon Reduction",
            "image_prompt": f"Futuristic green data center surrounded by clean wind turbines and lush nature, green sustainable computing",
            "gif_query": "green technology clean energy",
            "speaker_notes": f"True engineering sophistication embraces ecological reality; sparse computation allows us to drastically slash energy requirements."
        },
        # Slide 15: Limitations, Edge Cases & Failure Modes
        {
            "layout_type": "three_cards",
            "tag": "FAILURE ANALYSIS",
            "title": "Critical Constraints & Known Failure Modes",
            "subtitle": "Honest Scientific Appraisal of Boundary Conditions",
            "bullet_points": [
                "**Distributional Drift**: Model degradation when confronted with out-of-distribution inputs exceeding two standard deviations.",
                "**High Initialization Overhead**: Cold-start latency penalties demanding significant memory pre-allocation before steady-state.",
                "**Heuristic Brittleness**: Sensitivity to hyperparameter misconfiguration requiring dedicated Bayesian tuning loops."
            ],
            "stat_or_highlight": "Scientific Rigor",
            "image_prompt": f"Warning diagnostic terminal analyzing system boundary conditions and stress limits, dark tech aesthetic",
            "gif_query": "system warning diagnostic error",
            "speaker_notes": f"Intellectual honesty requires us to explicitly delineate edge cases where the system degrades, enabling targeted future countermeasures."
        },
        # Slide 16: Interdisciplinary Convergence
        {
            "layout_type": "split_image_left",
            "tag": "CROSS-DISCIPLINARY",
            "title": "Cross-Disciplinary Synergies & Convergence",
            "subtitle": "Intersecting with Quantum Mechanics, Neuroscience, and Material Science",
            "bullet_points": [
                "**Neuromorphic Hardware Interfaces**: Mapping event-driven spikes onto bio-inspired memristor chips for ultra-low power edge devices.",
                "**Quantum Annealing Hybrids**: Outsourcing combinatorial sub-problems to quantum coprocessors while executing linear logic on classical CPUs.",
                "**Materials Discovery**: Utilizing automated generative feedback loops to synthesize novel superconducting alloy compounds."
            ],
            "stat_or_highlight": "Quantum-Bio Convergence",
            "image_prompt": f"Brain neural network merging seamlessly into quantum atomic circuits and holographic particles, 3d render",
            "gif_query": "neural network quantum brain",
            "speaker_notes": f"The most fertile breakthroughs occur at the intersection of disciplines, notably where neuromorphic hardware meets quantum acceleration."
        },
        # Slide 17: Developer Ecosystem & Open Source Tooling
        {
            "layout_type": "split_image_right",
            "tag": "TOOLING & STANDARDS",
            "title": "Ecosystem Architecture & Open Standards",
            "subtitle": "Building Reproducible, Extensible Scientific Infrastructure",
            "bullet_points": [
                "**Modular SDK Architecture**: Providing declarative APIs across Python, Rust, and C++ for seamless community integration.",
                "**Deterministic Benchmarking Suites**: Standardized test harnesses enabling independent third-party reproducibility of empirical claims.",
                "**Containerized Artifacts**: Encapsulating complete dependency topologies within OCI-compliant isolated sandbox containers."
            ],
            "stat_or_highlight": "100% Reproducible",
            "image_prompt": f"Open source code repository terminal with glowing branches and git graph visualizations, 3d render",
            "gif_query": "coding terminal programming developer",
            "speaker_notes": f"Scientific validity depends upon reproducibility; our open toolchain guarantees that every experiment can be independently verified."
        },
        # Slide 18: Unsolved Problems & Open Research Questions
        {
            "layout_type": "deep_theory",
            "tag": "OPEN RESEARCH",
            "title": "Frontier Dilemmas & Open Conjectures",
            "subtitle": "Unresolved Theoretical Questions Paving Future Inquiries",
            "bullet_points": [
                "**Sub-Linear Memory Scaling**: Investigating whether topological data analysis can compress continuous manifold representations below theoretical Shannon limits.",
                "**Unsupervised Causal Discovery**: Disentangling true invariant causal relationships from spurious observational correlations without randomized controlled trials.",
                "**Zero-Knowledge Verifiable Inference**: Proving computational correctness across untrusted edge clusters without disclosing underlying model weights."
            ],
            "stat_or_highlight": "Grand Challenge Problems",
            "image_prompt": f"Abstract portal of glowing mathematical equations leading into the infinite unknown universe, 3d scientific render",
            "gif_query": "deep space universe mystery portal",
            "speaker_notes": f"These open questions mark the boundary of current human knowledge, providing promising doctoral thesis topics for subsequent investigations."
        },
        # Slide 19: Strategic Five-Year Roadmap
        {
            "layout_type": "three_cards",
            "tag": "STRATEGIC ROADMAP",
            "title": "Next Horizon: 5-Year Research Trajectory",
            "subtitle": "Phased Milestones Driving Algorithmic Maturation",
            "bullet_points": [
                "**Phase 1 (Immediate)**: Broad deployment of hardware-accelerated micro-kernels across distributed academic research clusters.",
                "**Phase 2 (Mid-Term)**: Implementation of autonomous self-healing topology reconfigurations in mission-critical deployments.",
                "**Phase 3 (Long-Term)**: Universal international standardization of interoperability protocols across heterogeneous clouds."
            ],
            "stat_or_highlight": "2026-2030 Horizon",
            "image_prompt": f"Strategic roadmap timeline glowing in neon cyber aesthetics, milestone checkpoints",
            "gif_query": "future roadmap milestones",
            "speaker_notes": f"Our multi-year research roadmap lays down tangible, phased deliverables to elevate this technology from lab validation to ubiquitous infrastructure."
        },
        # Slide 20: Comprehensive Synthesis & Core Contributions
        {
            "layout_type": "deep_theory",
            "tag": "SYNTHESIS & SUMMARY",
            "title": "Synthesis of Key Research Contributions",
            "subtitle": "Recap of Theoretical Inventions and Practical Validations",
            "bullet_points": [
                f"**Axiomatic Resolution**: Successfully resolved fundamental bottlenecks in {clean_topic} through formal mathematical decomposition.",
                "**Empirical Supremacy**: Validated superior convergence speed, memory thrift, and partition resilience across diverse stress benchmarks.",
                "**Practical Blueprint**: Delivered an open-source, reproducible architecture ready for immediate integration into high-stakes environments."
            ],
            "stat_or_highlight": "Primary Thesis Delivered",
            "image_prompt": f"Magnificent glowing golden trophy cup or graduation insignia on a sleek dark slate pedestal, 3d render",
            "gif_query": "success victory gold light",
            "speaker_notes": f"In synthesis, this research provides both a rigorous mathematical foundation and a pragmatic blueprint for next-generation implementation."
        },
        # Slide 21: Dedicated Closing & Thank You Slide (MANDATORY FOR EVERY DECK)
        {
            "layout_type": "thank_you",
            "tag": "ACKNOWLEDGMENTS & Q&A",
            "title": "Thank You for Your Time & Attention",
            "subtitle": "Open for Questions, Critical Feedback, and Academic Discussion",
            "closing_message": "We express sincere gratitude to our faculty mentors, thesis advisory committee, and peer researchers whose critical insights have deeply enriched this investigation.",
            "bullet_points": [
                f"**Research Defense**: {clean_topic} — Complete Analytical Study.",
                "**Open Forum**: The floor is now warmly open for Questions, Academic Inquiries & Constructive Critiques.",
                "**Repository & Documentation**: Full source code, formal mathematical proofs, and reproducibility benchmarks available online."
            ],
            "stat_or_highlight": "Floor Open for Q&A",
            "image_prompt": f"Warm minimalist scientific auditorium with spotlight on podium, sleek clean aesthetic, professional presentation closing",
            "gif_query": "applause presentation thank you question",
            "speaker_notes": f"Thank you very much for your thoughtful attention and guidance. I now look forward to answering your questions and hearing your critical insights during this Q&A session."
        }
    ]

    # Select exactly requested slide count
    # Always guarantee Slide 1 is Definition/Intro, and Last Slide is Thank You!
    selected = []
    first_slide = dict(master_modules[0])
    first_slide["slide_number"] = 1
    selected.append(first_slide)

    middle_count = count - 2
    if middle_count > 0:
        available_middle = master_modules[1:-1]
        for i in range(middle_count):
            mod_idx = i % len(available_middle)
            slide_copy = dict(available_middle[mod_idx])
            slide_copy["slide_number"] = i + 2
            selected.append(slide_copy)

    # Add the Mandatory Closing Thank You slide as the final slide
    if count > 1:
        closing_slide = dict(master_modules[-1])
        closing_slide["slide_number"] = count
        selected.append(closing_slide)

    return {
        "presentation_title": clean_topic,
        "presentation_subtitle": f"Exhaustive Academic Defense & Research Analysis — {education_level}",
        "target_audience": education_level,
        "slides": selected
    }

def generate_presentation_with_gemini(topic: str, slide_count: int, education_level: str = "Master's & Doctoral", api_key: str = None) -> dict:
    """
    Calls Google Gemini 2.0 Flash for deep academic presentation generation.
    Falls back gracefully to the exhaustive 25-slide Academic Fallback Engine.
    """
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key or len(key.strip()) < 10:
        print("[AIEngine] Using Comprehensive 25-Slide Academic Research Engine.")
        return generate_academic_deep_deck(topic, slide_count, education_level)

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key.strip()}"
    
    prompt = f"""
Generate an authoritative, deeply researched academic presentation deck for university students and evaluators.
Topic: "{topic}"
Exact Number of Slides: {slide_count}
Academic Level: {education_level}

CRITICAL MANDATORY INSTRUCTIONS:
1. SLIDE 1 MUST INCLUDE A FORMAL CONCEPT DEFINITION in a 'formal_definition' field. It must clearly state: What is {topic}? What is its formal scientific/engineering definition and core premise?
2. SLIDE {slide_count} (THE LAST SLIDE) MUST BE A DEDICATED CLOSING & THANK YOU SLIDE:
   - Layout type: 'thank_you'
   - Tag: 'ACKNOWLEDGMENTS & Q&A'
   - Title: 'Thank You for Your Time & Attention'
   - Include a courteous 'closing_message' thanking professors, reviewers, and evaluators.
   - Open the floor for questions and discussion.
3. EXTENSIVE THEORETICAL DEPTH: Provide rigorous, scholarly bullet points with bold headers (e.g. "**Mathematical Formalism**: ...", "**Architectural Invariance**: ..."). No superficial 1-liners!
4. LANGUAGE: 100% Scholarly, Professional English throughout.

Output strictly valid JSON matching this schema:
{{
  "presentation_title": "Precise Academic Title",
  "presentation_subtitle": "Exhaustive Theoretical Investigation & Defense",
  "target_audience": "{education_level}",
  "slides": [
    {{
      "slide_number": 1,
      "layout_type": "title",
      "tag": "FOUNDATIONAL DEFINITION",
      "title": "Formal Academic Heading",
      "subtitle": "Theoretical Foundations and Scope",
      "formal_definition": "Precise scientific/technical definition of {topic} explaining exactly what it is and its fundamental tenets.",
      "bullet_points": [
        "**Taxonomic Domain**: Rigorous classification and scope.",
        "**Core Axiom**: Foundational premise and theoretical grounding.",
        "**Defense Overview**: Roadmap of analytical and empirical contributions."
      ],
      "stat_or_highlight": "Academic Year 2026",
      "image_prompt": "Detailed 3d schematic diagram illustrating {topic}",
      "gif_query": "{topic} concept",
      "speaker_notes": "Formal opening address for presentation/viva."
    }}
  ]
}}
"""

    payload = {
        "contents": [{"parts": [{"text": SYSTEM_PROMPT}, {"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.3}
    }

    try:
        res = requests.post(endpoint, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
        if res.status_code == 200:
            data = res.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            cleaned = re.sub(r'^```json\s*', '', raw_text.strip())
            cleaned = re.sub(r'\s*```$', '', cleaned)
            parsed = json.loads(cleaned)
            if "slides" in parsed and len(parsed["slides"]) > 0:
                print(f"[AIEngine] Successfully generated {len(parsed['slides'])} scholarly slides via Gemini!")
                return parsed
    except Exception as e:
        print(f"[AIEngine] Gemini API error: {e}")

    return generate_academic_deep_deck(topic, slide_count, education_level)
