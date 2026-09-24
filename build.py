from pathlib import Path
import json, html, re

ROOT=Path(__file__).resolve().parent
D=ROOT
def esc(s): return html.escape(str(s),quote=True)
def link(url,label): return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)} <span aria-hidden="true">↗</span></a>'
def bullets(items): return '<ul>'+''.join('<li>'+s+'</li>' for s in items)+'</ul>'
def ongoing_tag(meta, tag):
    if 'Present' in meta and 'Ongoing' not in tag:
        return (tag + ' · ' if tag else '') + 'Ongoing'
    return tag

def metadata(meta):
    parts = re.split(r' · |<br>', meta)
    return ''.join('<span class="meta-line'+(' date-line' if re.search(r'\b(?:19|20)\d{2}\b', re.sub('<[^>]+>', '', part)) and not part.startswith('<strong>') else '')+'">'+part+'</span>' for part in parts)

def entry(title,meta,body='',tag='',links=[]):
    tag = ongoing_tag(meta, tag)
    return f'<article class="entry"><div class="entry-top"><h3>{title}</h3>'+ (f'<span class="tag">{tag}</span>' if tag else '')+f'</div><div class="meta">{metadata(meta)}</div>{body}'+(f'<div class="links">'+''.join(link(u,l) for u,l in links)+'</div>' if links else '')+'</article>'
def section(id,num,title,body,intro=''):
    return f'<section id="{id}" class="section"><div class="section-heading"><span>{num}</span><h2>{title}</h2></div>'+ (f'<p class="section-intro">{intro}</p>' if intro else '')+body+'</section>'

papers=[
dict(kind='Manuscript in preparation',title='LoRA-MAS: Trustworthy AI through Evidence-Governed Multi-Agent Reasoning',authors='Liao, C.-L., & Chen, L.-F.',venue='2026 · Planned submission to Omega – The International Journal of Management Science (SCIE/SSCI; JCR Q1) · Special Issue on Data-Enabled Analytics for Insightful and Responsible Decision-Making',note='',details=[
'Developed an evidence-governed LoRA multi-agent framework with four QLoRA adapters and eight heterogeneous virtual experts, integrating human-in-the-loop evidence governance, provenance tracking, and confidence-aware AHP elicitation.',
'Designed a white-box decision-assurance pipeline combining reciprocity-preserving Z-number uncertainty modeling, consistency-ratio auditing, and deterministic logarithmic least-squares repair for traceable and mathematically controlled AI-assisted decision making.',
'Reported Spearman ρ = 0.925, Kendall τ = 0.878, Pearson r = 0.976, and 100% Top-5 agreement with published Supply Chain 5.0 human-expert results. Conducted cross-domain boundary audits on Project Management and Medical Alliance benchmarks.'],links=[('https://www.sciencedirect.com/special-issue/10GMWX3GDSQ','Omega special issue')]),
dict(kind='Submitted',title='Simulation-Based Operating-Window Optimization for Lithium-Ion Batteries Using Taguchi Design, Surrogate Modeling, and Multi-Algorithm Search',authors='Liao, C.-L. · Sole author',venue='Submitted to the International Journal of Innovative Computing, Information and Control (IJICIC) (ESCI; JCR Q4; Scopus Q2)',note='Submitted.',details=[
'Independently designed and executed a battery operating-window study combining a verified Taguchi L27 design, 27,000 Monte Carlo simulation samples, surrogate modeling, and constrained multi-algorithm optimization.',
'Redesigned validation to address leakage from repeated samples under identical operating conditions: five-fold GroupKFold by Taguchi condition measures generalization to unseen operating windows.',
'Compared linear, kernel-based, tree-based, Gaussian-process, ANN, RSM, and physics-informed RSM surrogates, followed by GA, PSO, Differential Evolution, Bayesian Optimization, NSGA-II, and grid-search optimization. Evaluated coefficient, weighting, and noise sensitivity.',
'In simulation, service-aware optimization shifted the optimal charging rate from 1.00 C to 1.50 C, while maintaining 1.00 C discharge, 20 °C, and approximately 50% SOC. At 300 cycles, PSO achieved 87.57% capacity retention and 58.34 mΩ internal resistance: a 1.025 percentage-point capacity penalty and 0.502 mΩ resistance increase relative to the degradation-only optimum.',
'Earlier version: externally peer reviewed at Expert Systems (Wiley), with three reviewer reports, including one recommendation for major revision. The manuscript was subsequently substantially revised in response to the reviews, with expanded surrogate and optimizer baselines, leakage-aware validation, multi-objective weighting analysis, noise-robustness evaluation, stronger research-gap positioning, and improved methodological reporting. The current manuscript has been submitted to IJICIC.'],links=[('http://www.ijicic.org/','IJICIC journal website')]),
dict(kind='Submitted · Full paper',title='Traceable Spec-RAG for Evidence-Grounded Binary Parser Synthesis',authors='Liao, C.-L., Wu, C.-H., & Wu, S.-D.',venue='31st International Conference on Technologies and Applications of Artificial Intelligence (TAAI 2026) · New Taipei City, Taiwan · Conference expected to take place on November 20–21, 2026',note='Submitted. Acceptance pending. The paper will be submitted for selection for inclusion in the post-proceedings published in Springer’s Communications in Computer and Information Science (CCIS) series. The CCIS series is indexed in Scopus, EI Compendex, and DBLP.',details=[
'Proposed a structure-aware, field-oriented Spec-RAG framework to convert heterogeneous, versioned protocol specifications into traceable binary parser schemas through structured evidence representation and field-specific retrieval.',
'Built an evidence pipeline with hybrid retrieval, protocol-version filtering, field-level coverage and conflict checks, provenance tracking, and no-evidence / bounded-repair mechanisms to prevent unsupported or cross-protocol parser generation.',
'Reported 100% schema exactness and strict balanced accuracy in a controlled two-protocol, execution-based benchmark, with 37.8% lower token usage than vanilla RAG under constrained repeated runs.'],links=[('https://taai2026.github.io/','Conference website'),('https://link.springer.com/series/7899','CCIS series & indexing')]),
dict(kind='Gold Award · Poster',title='Real-Time Lung Tumor Segmentation via Edge-Collaborative IoT for Enhanced Clinical Quality',authors='Liao, C.-L., & Wu, S.-D.',venue='2026 Medical Quality Conference · Taiwan · Full paper and poster presentation',note='Gold Award, Poster Competition.',details=[
'Proposed a modality-aware CT preprocessing pipeline combining HU-based lung windowing, axial slice transformation, and tumor-positive sample selection to adapt volumetric medical imaging for lightweight edge segmentation.',
'Controlled ablation showed a 22.5 percentage-point improvement in mAP50 over the unfiltered baseline when preprocessing components were combined.',
'Demonstrated the pipeline in an edge-collaborative medical IoT architecture that connects segmentation outputs to event-driven clinical alerts.'],links=[('https://www.6sigmai.org/general-6-1','Official award list')]),
dict(kind='Paper · Oral presentation',title='Optimizing BMS Models to Minimize Heat Generation and Energy Loss for Enhanced Overall System Efficiency',authors='Liao, C.-L., & Liao, H.-C.',venue='24th Annual Hawaii International Conference on Education (HICE 2026) · Honolulu, HI, USA · January 8–11, 2026',note='STEM Education session · Presentation: January 9, 2026.',details=[],links=[('https://hiceducation.org/wp-content/uploads/2025/12/2026-Tentative-Program.pdf','Official program (PDF)')]),
dict(kind='Paper · Oral presentation',title='Enhancing the Understanding of Vector Calculus in Engineering Education Using Matplotlib for Visualization and Problem Solving',authors='Liao, C.-L., & Wang, Y.',venue='23rd Annual Hawaii International Conference on Education (HICE 2025) · Honolulu, HI, USA · January 4–7, 2025',note='STEM Education session.',details=[],links=[('https://hiceducation.org/wp-content/uploads/2025/12/EDU2025.pdf','Official program (PDF)')]),
dict(kind='Accepted',title='Simulation-Based Screening of Lithium-Ion Battery Operating Windows Under Degradation and Service Constraints',authors='Liao, C.-L. · Sole author',venue='2026 International Conference on Green Electrochemical Technologies (ICGET-Tw 2026) · Taoyuan, Taiwan · Conference expected to take place on November 6–8, 2026',note='Accepted — Poster Competition for Student.',details=[],links=[('https://2026icget-tw.conf.tw/site/page.aspx?lang=en&pid=901&sid=1672','Conference website')]),
dict(kind='Abstract · Oral presentation',title='Visualization and Simulation Analysis of Battery Management System Based on Thermodynamic Models',authors='Liao, C.-L., & Liao, H.-C.',venue='2025 WEI International Academic Conference on Technology and Science Education · Harvard Faculty Club, Boston, MA, USA · July 22–24, 2025',note='Conference abstract and oral presentation. Venue: Harvard Faculty Club.',details=[],links=[('https://www.westeastinstitute.com/wp-content/uploads/2025/10/EDUHUMSCIENCE-2025-Boston-Proceedings.pdf','Official proceedings (PDF)')])
]

def research_entry(title, meta, body='', tag='', links=[]):
    tag = ongoing_tag(meta, tag)
    parts = meta.split(' · ')
    role = parts.pop(0)
    facts = metadata(' · '.join(parts))
    return ('<article class="entry research-entry"><div class="research-entry-header">'
            '<h3 class="research-role">'+role+'</h3>'
            + ('<span class="tag">'+tag+'</span>' if tag else '')
            + '</div><p class="research-topic">'+title+'</p>'
            + '<div class="meta research-facts">'+facts+'</div>'
            + '<div class="research-description">'+body+'</div>'
            + ('<div class="links">'+''.join(link(u,l) for u,l in links)+'</div>' if links else '')
            + '</article>')

def teaching_entry(title, meta, body='', tag='', links=[]):
    tag = ongoing_tag(meta, tag)
    parts = meta.split(' · ')
    role = parts.pop(0)
    facts = metadata(' · '.join(parts))
    return ('<article class="entry teaching-entry"><div class="teaching-entry-header">'
            '<h3 class="teaching-role">'+role+'</h3>'
            + ('<span class="tag">'+tag+'</span>' if tag else '')
            + '</div><p class="teaching-topic">'+title+'</p>'
            + '<div class="meta teaching-facts">'+facts+'</div>'
            + '<div class="teaching-description">'+body+'</div>'
            + ('<div class="links">'+''.join(link(u,l) for u,l in links)+'</div>' if links else '')
            + '</article>')

research=research_entry('Explainable AI for Risk Assessment','Research Assistant · Li-Fei Chen Research Group, NTNU · August 2026 – Present (expected to end in January 2027) · Advisor: Prof. Li-Fei Chen','<p>NSTC-funded faculty research project: <em>Leveraging AI–ESG Synergies to Enhance Corporate Competitiveness.</em></p><p>Research context includes machine learning, decision analytics, explainable AI, and mathematical modeling.</p>','Ongoing')
research+=research_entry('Market-Integrated CPS: A CSTAL-MoE Framework for Intelligent Steel ESG Management','NSTC College Student Research Scholarship · July 1, 2026 – Present (expected to end on February 28, 2027) · Advisor: Prof. Li-Fei Chen','<p>Funded undergraduate research supported by the National Science and Technology Council (NSTC), Taiwan.</p>','Ongoing')
research+=research_entry('Agentic AI, RAG & Edge AI for Real-World Deployment','Research Assistant · Signal Processing Lab, NTNU · October 2025 – August 2026 · Advisor: Prof. Shuen-De Wu','<p>Industry–academia AIoT research integrating LLM-based agentic AI, retrieval-augmented generation, and Edge AI. Research areas include computer vision and embedded systems.</p>')

pubs=''
for group,inds in [('Journal Papers',[0,1]),('Conference Papers & Presentations',[2,6,3,4,7,5])]:
    pubs+=f'<h3 class="group-title">{group}</h3>'
    for i in inds:
        p=papers[i]
        detail=f'<p class="paper-note">{esc(p["note"])}</p>' if p['note'] else ''
        if p['details']: detail+='<details><summary>Research contributions & results</summary>'+bullets([esc(x) for x in p['details']])+'</details>'
        pubs+=entry(esc(p['title']),f'<strong>{esc(p["authors"])}</strong><br>{esc(p["venue"])}',detail,p['kind'],p['links'])

experience=entry('AI Application Product R&D Engineer Intern','Octon International Technology Corporation · Part-time · Taipei, Taiwan · August 2026 – Present',bullets([
'Contribute to R&D and validation of Orion AI Orchestrator, an enterprise agentic AI platform covering agent selection, workflow control, tool routing, RAG, AI governance, and enterprise integration.',
'Support LLM/RAG, NLP, and ASR-enabled customer-service workflows, including multi-format knowledge ingestion, semantic retrieval, speech recognition, and AI-assisted response generation.',
'<strong>Project:</strong> Orion AI Orchestrator — a multi-agent backend collaboration platform for customer service at BankTaiwan Life Insurance.',
'<strong>Project:</strong> Enterprise RAG solutions — FamilyMart.',
'Invited by Prof. Charles Chan to join Octon after presenting my first-author lung-tumor segmentation research in his Artificial Intelligence and Life course.']),links=[('https://www.octon.net/zh/','Company website')])
experience+=entry('Research Engineer Intern','Ucore Technology Inc. · Part-time · Taipei, Taiwan · October 2025 – Present (expected to end in January 2027)',bullets([
'Develop and validate applied AI for public infrastructure and industrial environments, including computer vision, intelligent annotation, RAG, and multi-agent workflows.',
'<strong>Project:</strong> AI Sewer Pipeline Anomaly Detection — Sewerage Systems Office.',
'<strong>Project:</strong> AI Water-Quality Monitoring — Kbro × New Taipei City Environmental Protection Department.',
'<strong>Project:</strong> AI Occupational-Safety Recognition — Taipei Water Department.',
'<strong>Project:</strong> Audie AI Multi-Agent Document Review System — MOEA Value Creation Program.']),links=[('https://ucore.com.tw/','Company website')])
experience+=entry('Data Analysis & Research Intern','Chinese Society for Six Sigma · Part-time · Taipei, Taiwan · September 2024 – January 2026','<p>Supported data analysis, data organization, and research activities through structured analytical workflows and research execution.</p>',links=[('https://www.6sigmai.org/','Organization website')])

teaching=teaching_entry('Programming (MTU0012)','Teaching Assistant · <a href="https://en.ntnu.edu.tw/aboutus.php" target="_blank" rel="noopener noreferrer">National Taiwan Normal University</a> · September 2026 – Present (expected to end in January 2027)','<p class="small-facts">Instructor: Prof. Shuen-De Wu<br>C · Sole teaching assistant · Approximately 30 students · 3 hours/week</p>'+bullets(['Author detailed web-based solution guides, grade quizzes, and assist with introductory C programming instruction.','Provide post-class support in programming concepts, debugging, and problem solving.']),'Ongoing',links=[('https://chunlinliaoglobal-code.github.io/NTNU-programing-web-2026/','Teaching website'),('https://courseap2.itc.ntnu.edu.tw/acadmOpenCourse/SyllabusCtrl?year=115&term=1&courseCode=MTU0012&courseGroup=B&deptCode=HU73&formS=1&classes1=&deptGroup=','Course syllabus')])
teaching+=teaching_entry('Digital Logic Design Laboratory (MTU0100)','Teaching Assistant · <a href="https://en.ntnu.edu.tw/aboutus.php" target="_blank" rel="noopener noreferrer">National Taiwan Normal University</a> · February – June 2026','<p class="small-facts">Instructor: Prof. Shuen-De Wu<br>Verilog HDL · DE0-Nano FPGA · Team of 2 TAs · Approximately 30 students · 3 hours/week</p>'+bullets(['Recorded supplementary instructional materials on pin assignments and FPGA programming, authored detailed web-based solution guides, graded assignments, and led FPGA laboratory sessions.','Guided Verilog HDL and DE0-Nano FPGA development, including a final traffic-light controller project and a digital clock project, debugging, and post-class technical support.']),links=[('https://chunlinliaoglobal-code.github.io/NTNU_digital-logic-design-lab_web/','Teaching website'),('https://courseap2.itc.ntnu.edu.tw/acadmOpenCourse/SyllabusCtrl?year=114&term=2&courseCode=MTU0100&courseGroup=A&deptCode=HU73&formS=1&classes1=&deptGroup=','Course syllabus')])
teaching+=teaching_entry('Undergraduate Capstone Projects','Technical Mentor · Mentored five junior students','<p>Created introductory materials on LLMs, image recognition, and IoT fundamentals. Guided computer vision, RAG, and IoT temperature-sensor projects through implementation, troubleshooting, and development.</p>')

education=entry('<a href="https://en.ntnu.edu.tw/aboutus.php" target="_blank" rel="noopener noreferrer">National Taiwan Normal University</a>','B.S. in Mechatronic Engineering · 2024 – Present (expected to graduate in June 2027)','<p>Transferred from National Taiwan Ocean University after completing Year 1.</p>')+entry('National Taiwan Ocean University','Department of Mechanical and Mechatronic Engineering · 2023 – 2024','<p>Completed Year 1 before transferring to NTNU.</p>')+entry('Taichung First Senior High School','High School Diploma')
courses=[('Undergraduate / master’s','Semiconductor Device Physics','A'),('Undergraduate / master’s','Big Data Analysis: Theory and Practice','A+'),('Undergraduate / master’s','Applied Machine Learning','Ongoing'),('Undergraduate / master’s','Digital Image Processing','Ongoing'),('Undergraduate / master’s','Nanotechnology','A+'),('Master’s / doctoral','Decision Theory and Analysis','A'),('Master’s / doctoral','Deep Learning','Ongoing'),('Master’s / doctoral','Reinforcement Learning','Ongoing')]
education+='<h3 class="group-title">Advanced Coursework</h3><div class="table-wrap"><table><caption>Jointly offered courses and reported grades</caption><thead><tr><th>Course level</th><th>Course</th><th>Grade / status</th></tr></thead><tbody>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in courses)+'</tbody></table></div>'
skills={'Programming':'Python, C, MATLAB, Verilog HDL','AI / ML':'PyTorch, CUDA, Computer Vision, LangChain, LangGraph','Systems':'Linux, Git, Docker, FastAPI, MQTT','Embedded platforms':'Genio 1200, nRF54L15, Arduino, DE0-Nano FPGA'}
education+='<h3 class="group-title">Technical skills</h3><dl class="skills">'+''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k,v in skills.items())+'</dl>'

awards=entry('NSTC College Student Research Scholarship','National Science and Technology Council, Taiwan · 2026')+entry('Gold Award — Poster Competition','2026 Medical Quality Conference · 2026',links=[('https://www.6sigmai.org/general-6-1','Official award list')])
professional=[('2026','Virtual U.S.–Taiwan–Japan Semiconductor Collaboration Program by AIT','Policy, technology, and talent development.'),('September 2025','TSMC Semiconductor Cloud Academy','Semiconductor technology training.'),('Completed','Academic Research Ethics','Taiwan Academic Ethics Education Resource Center · 9 hours 20 minutes · Passed.'),('2025','SEMICON Taiwan','Semiconductor fabrication and precision instrument technologies.'),('2025','NSTC Medical Education Symposium','AI image recognition and AI in medical devices.'),('October 2025','MathWorks Webinar','Model, Simulate, and Analyze Faults for Battery System')]
professional = [professional[i] for i in [0,5,1,3,4,2]]
education+='<h3 class="group-title">Training & professional activities</h3><ul class="activities">'+''.join(f'<li><span class="activity-date">{a}</span><div><strong>{b}</strong><p>{c}</p></div></li>' for a,b,c in professional)+'</ul>'
leadership=entry('NTU Coconut Wind Rock Club','Keyboardist','<p>Performed on keyboards and contributed to band rehearsals, arrangements, and collaborative music projects.</p>')+entry('Taichung First Senior High School Hot Music Club','President & Keyboardist','<p>Led club operations and coordinated campus and off-campus performances, including rehearsal planning, scheduling, and team coordination.</p>')+entry('Table Tennis Team','Taichung First Senior High School','<p>Participated in regular team training and inter-school competitions.</p>')+entry('Music Production & Arrangement','Independent practice','<p>Self-taught Logic Pro, digital music production, arrangement, keyboard performance, and music programming tools, with experience producing and arranging original music projects.</p>')

sections=section('research','01','Research experience',research)+section('publications','02','Publications & Presentations',pubs)+section('experience','03','Internships',experience)+section('teaching','04','Teaching & Mentoring',teaching)+section('education','05','Education & Training',education)+section('awards','06','Honors & Awards',awards)+section('leadership','07','Beyond Research',leadership)
contact='<a href="mailto:chunlin.liao.global@gmail.com">chunlin.liao.global@gmail.com</a><a href="mailto:41373902h@gapps.ntnu.edu.tw">41373902h@gapps.ntnu.edu.tw</a><a href="https://www.linkedin.com/in/chun-lin-liao-755b65386/" target="_blank" rel="noopener noreferrer">LinkedIn <span aria-hidden="true">↗</span></a>'
about='''<section id="about" class="intro"><h1>Chun-Lin Liao</h1><p class="lead">Trustworthy agentic AI.<br>Evidence-grounded decisions.</p><h2 class="about-label">Research focus</h2><p>I am an undergraduate researcher in Mechatronic Engineering at <a href="https://en.ntnu.edu.tw/aboutus.php" target="_blank" rel="noopener noreferrer">National Taiwan Normal University</a>, with an expected graduation date of June 2027. My research focuses on trustworthy agentic AI and AI-enabled decision systems, particularly evidence-grounded reasoning and explainable, uncertainty-aware decision making. I connect these interests to real-world AI applications through AIoT (Artificial Internet of Things), integrating AI models with sensors, embedded systems, and edge devices.</p><h2 class="about-label">Research mentorship</h2><p>I am currently advised by Prof. Li-Fei Chen and Prof. Shuen-De Wu. With Prof. Chen, I study machine learning, decision analytics, explainable AI, and mathematical modeling through research on AI-based risk assessment. With Prof. Wu in the Signal Processing Lab, I work on LLM-based agentic AI, retrieval-augmented generation (RAG), and Edge AI for real-world deployment, including computer vision and embedded systems.</p><h2 class="about-label">Current work</h2><p>My current research centers on <strong>LoRA-MAS: Trustworthy AI through Evidence-Governed Multi-Agent Reasoning</strong>, combining multi-agent reasoning with traceable evidence and uncertainty-aware decision making. Alongside this work, I am developing an <strong>agentic IoT platform</strong> that connects LLM-based agents, retrieval-augmented generation, and connected devices for real-world AI applications.</p><p>In a separate line of research, I have submitted <strong>Simulation-Based Operating-Window Optimization for Lithium-Ion Batteries Using Taguchi Design, Surrogate Modeling, and Multi-Algorithm Search</strong>, investigating battery operating conditions through simulation, surrogate modeling, and constrained optimization. A distinct NSTC-funded undergraduate project, <strong>Market-Integrated CPS: A CSTAL-MoE Framework for Intelligent Steel ESG Management</strong>, focuses on intelligent steel ESG management.</p><p>These research interests also inform my industry work: after I presented my first-author lung-tumor segmentation research in his Artificial Intelligence and Life course, <strong>Prof. Charles Chan invited me to join Octon</strong>. There, as an AI Application Product R&amp;D Engineer Intern, I contribute to <strong>Orion AI Orchestrator, a multi-agent backend collaboration platform for customer service at BankTaiwan Life Insurance</strong>, working on agent workflows and tool routing. In a separate project, I contribute to <strong>enterprise RAG solutions for FamilyMart</strong>, focusing on enterprise knowledge retrieval. At <strong>Ucore</strong>, my role as a Research Engineer Intern focuses on applied AI for public infrastructure, including computer vision for pipeline inspection, water-quality monitoring, occupational safety, and multi-agent document review.</p><div class="topic-list"><span>Agentic AI & RAG</span><span>Explainable decision systems</span><span>Edge AI & AIoT</span><span>Real-world AI applications</span></div><div class="intro-links"><a class="button" href="#publications">Explore my research <span aria-hidden="true">↓</span></a><a class="text-button" href="cv.html" target="_blank">View / print CV <span aria-hidden="true">↗</span></a></div></section>'''
nav=[('about','About Me'),('research','Research Experience'),('publications','Publications & Presentations'),('experience','Internships'),('teaching','Teaching & Mentoring'),('education','Education & Training'),('awards','Honors & Awards'),('leadership','Beyond Research')]
head='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="Chun-Lin Liao — NTNU undergraduate researcher in trustworthy agentic AI, evidence-grounded decision systems, and Edge AI. Research, publications, teaching, and experience."><meta name="theme-color" content="#193f4a"><title>Chun-Lin Liao | Academic Portfolio</title><link rel="icon" href="assets/favicon.svg?v=2" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/refinements.css"><link rel="stylesheet" href="assets/themes.css?v=6"><link rel="stylesheet" href="assets/navigation.css?v=9"><link rel="stylesheet" href="assets/polish.css?v=14"><script src="assets/theme.js?v=6"></script></head>'''
sidebar='''<aside class="profile"><div class="portrait-frame"><img class="portrait" src="assets/profile.jpg" alt="Formal studio portrait of Chun-Lin Liao in a white shirt" width="256" height="260"></div><div class="profile-text"><a class="profile-name" href="#about">Chun-Lin Liao</a><p>Undergraduate Researcher<br>Mechatronic Engineering</p><p class="affiliation"><a href="https://en.ntnu.edu.tw/aboutus.php" target="_blank" rel="noopener noreferrer">National Taiwan<br>Normal University</a></p><div class="profile-meta"><span>Taipei, Taiwan</span></div><div class="profile-contact">'''+contact+'''</div></div><a class="cv-link" href="cv.html" target="_blank">Curriculum vitae <span aria-hidden="true">↗</span></a></aside>'''
footer='<footer><span>© 2026 Chun-Lin Liao</span></footer>'
live_band_gallery = '<div class="band-gallery-section" aria-labelledby="live-band-heading"><h2 id="live-band-heading" class="group-title">Off the Clock, On Stage</h2><div class="band-gallery"><a href="assets/live-band/live-band-01.jpg" target="_blank" rel="noopener noreferrer" class="band-photo" aria-label="View live band photo 1 at full size"><img src="assets/live-band/live-band-01.jpg" alt="Live band performance with keytar, guitar, and vocals under blue stage lighting" width="2048" height="1366" loading="lazy" decoding="async"></a><a href="assets/live-band/live-band-02.jpg" target="_blank" rel="noopener noreferrer" class="band-photo" aria-label="View live band photo 2 at full size"><img src="assets/live-band/live-band-02.jpg" alt="Live stage performance with keytar and keyboard under warm spotlights" width="434" height="578" loading="lazy" decoding="async"></a><a href="assets/live-band/live-band-03.jpg" target="_blank" rel="noopener noreferrer" class="band-photo" aria-label="View live band photo 3 at full size"><img src="assets/live-band/live-band-03.jpg" alt="Keyboard performance with a drummer in the background under blue lighting" width="2048" height="1362" loading="lazy" decoding="async"></a><a href="assets/live-band/live-band-04.jpg" target="_blank" rel="noopener noreferrer" class="band-photo" aria-label="View live band photo 4 at full size"><img src="assets/live-band/live-band-04.jpg" alt="Keyboard performance in a white shirt and tie under purple stage lighting" width="2048" height="1365" loading="lazy" decoding="async"></a></div></div>'
live_band_gallery += '<dialog class="band-lightbox" aria-label="Beyond Research photo viewer"><div class="band-viewer"><button type="button" class="band-close" aria-label="Close photo viewer">Close ×</button><img class="band-full" alt=""><div class="band-controls"><button type="button" class="band-prev" aria-label="Previous photo">← Previous</button><span class="band-count" aria-live="polite"></span><button type="button" class="band-next" aria-label="Next photo">Next →</button></div></div></dialog>'



# Keep the original performance photos and add a lighthearted caption to each.
band_captions = [
    'Good music, great company.',
    'A little stage light, a lot of energy.',
    'Finding my rhythm, one key at a time.',
    'Dressed up and ready to play.',
]
for i, caption in enumerate(band_captions, 1):
    start = live_band_gallery.index('<a href="assets/live-band/live-band-' + f'{i:02d}' + '.jpg"')
    end = live_band_gallery.index('</a>', start) + 4
    photo = live_band_gallery[start:end]
    live_band_gallery = live_band_gallery[:start] + '<figure class="band-frame">' + photo + f'<figcaption><span class="figure-number">Fig. {i}</span>{caption}</figcaption></figure>' + live_band_gallery[end:]

personal_gallery = '''<section class="band-gallery-section personal-gallery-section" aria-labelledby="personal-gallery-heading"><h2 id="personal-gallery-heading" class="group-title">Beyond the Resume</h2><div class="band-gallery personal-gallery"><figure class="band-frame"><a href="assets/beyond-research/studio-full-body.jpg" target="_blank" rel="noopener noreferrer" class="band-photo" aria-label="View full-length studio portrait at full size"><img src="assets/beyond-research/studio-full-body.jpg" alt="Full-length studio portrait of Chun-Lin Liao in a white shirt" width="1467" height="2200" loading="lazy" decoding="async"></a><figcaption><span class="figure-number">Fig. 1</span>A studio portrait marking the next step in my academic journey.</figcaption></figure><figure class="band-frame"><a href="assets/beyond-research/campus-visit.jpg" target="_blank" rel="noopener noreferrer" class="band-photo" aria-label="View campus visit photo at full size"><img src="assets/beyond-research/campus-visit.jpg" alt="Chun-Lin Liao standing on a university lawn in front of a campus building" width="2200" height="1650" loading="lazy" decoding="async"></a><figcaption><span class="figure-number">Fig. 2</span>A campus visit shaped by curiosity, exploration, and new possibilities.</figcaption></figure></div></section>'''

internship_figures = [
    ('Pipeline Annotation with LLM-Automated Workflows', 'A pipeline-inspection annotation system that combines model-assisted review with LLM-enabled workflow automation to organize and verify visual defect labels.', 'Pipeline annotation interface with LLM-assisted automation; project and account details redacted', 1813, 868),
    ('Binary Classification Training Results', 'Training-result visualizations used to compare classification outcomes, inspect error patterns, and support model evaluation for applied computer-vision tasks.', 'Binary classification training results comparing model outcomes in a twelve-panel plot', 945, 679),
    ('Audit AI — Corporate Auditing System', 'A corporate auditing interface developed for structured document review, supporting the applied multi-agent workflow research conducted at Ucore.', 'Ucore Audit AI corporate auditing system login interface', 1917, 908),
    ('Edge Computing with Genio 1200', 'A Genio 1200 development platform used to explore edge deployment for computer vision, embedded sensing, and real-world AI applications.', 'Genio 1200 development board for edge computing', 917, 768),
]
internship_gallery = '<section class="internship-gallery-section" aria-labelledby="internship-gallery-heading"><h2 id="internship-gallery-heading" class="group-title">From Ideas to Impact</h2><div class="internship-gallery">'
for i, (caption, description, alt, width, height) in enumerate([internship_figures[j] for j in (0, 2, 1, 3)], 1):
    image_path = f'assets/internships/project-{(1, 3, 2, 4)[i-1]:02d}.png'
    internship_gallery += f'<figure class="internship-figure"><a class="band-photo" href="{image_path}" target="_blank" rel="noopener noreferrer" aria-label="View figure {i}: {esc(caption)}"><img src="{image_path}" alt="{esc(alt)}" width="{width}" height="{height}" loading="lazy" decoding="async"></a><figcaption><span class="figure-number">Fig. {i}</span><strong>{esc(caption)}</strong><p class="figure-description">{esc(description)}</p></figcaption></figure>'
internship_additional_figures = [
    ('Pipeline Anomaly Recognition', 'An inspection workflow combining SAM 3.1 segmentation, YOLO transfer learning, and OCR-guided blurring for anomaly localization and privacy-aware visual processing.', 'Pipeline inspection results showing segmented anomalies identified with SAM 3.1 and YOLO transfer learning', 931, 663),
    ('Water-Color Recognition & Pollution Detection', 'Water-body segmentation and water-color recognition for detecting floating solids and other visible pollution.', 'Segmented water body with highlighted regions of visible pollution and floating waste', 1920, 1080),
]
for i, (caption, description, alt, width, height) in enumerate(internship_additional_figures, 5):
    image_path = f'assets/internships/project-{i:02d}.png'
    internship_gallery += f'<figure class="internship-figure"><a class="band-photo" href="{image_path}" target="_blank" rel="noopener noreferrer" aria-label="View figure {i}: {esc(caption)}"><img src="{image_path}" alt="{esc(alt)}" width="{width}" height="{height}" loading="lazy" decoding="async"></a><figcaption><span class="figure-number">Fig. {i}</span><strong>{esc(caption)}</strong><p class="figure-description">{esc(description)}</p></figcaption></figure>'
internship_gallery += '</div></section>'
internship_gallery += '<dialog class="band-lightbox" aria-label="Internship project photo viewer"><div class="band-viewer"><button type="button" class="band-close" aria-label="Close photo viewer">Close ×</button><img class="band-full" alt=""><div class="band-controls"><button type="button" class="band-prev" aria-label="Previous photo">← Previous</button><span class="band-count" aria-live="polite"></span><button type="button" class="band-next" aria-label="Next photo">Next →</button></div></div></dialog>'


publication_figures = [
    ('A Conversation That Inspired My PhD Journey', 'Meeting Princeton professor Michael Littman at a conference in Hawaii. Our conversation about electromagnetism inspired me to pursue a PhD.', 'Conference photograph with Prof. Michael Littman in Hawaii', 2048, 1536),
    ('Presenting Lung-Tumor Research', 'Poster presentation on lung-tumor segmentation at the Medical Quality Conference.', 'Lung-tumor segmentation poster presentation at the Medical Quality Conference', 1536, 2048),
    ('Agentic IoT Platform', 'System architecture integrating Spec-RAG, LLM-assisted parser generation, multimodal anomaly detection, and event-driven agent workflows.', 'Agentic IoT platform architecture diagram', 720, 402),
    ('Battery Operating-Window Study', 'Verified main effects on capacity retention and internal resistance from the L27 dataset (27,000 simulated observations). E represents the aging horizon, not an optimized BMS control variable.', 'Main-effects plots for charging current, discharging current, temperature, SOC, and aging horizon in the battery operating-window optimization study', 960, 526),
]
publication_gallery = '<section class="internship-gallery-section publication-gallery-section" aria-labelledby="publication-gallery-heading"><h2 id="publication-gallery-heading" class="group-title">Research in Focus</h2><div class="internship-gallery">'
for i, (caption, description, alt, width, height) in enumerate(publication_figures, 1):
    image_path = f'assets/publications/research-{i:02d}.png'
    publication_gallery += f'<figure class="internship-figure"><a class="band-photo" href="{image_path}" target="_blank" rel="noopener noreferrer" aria-label="View research figure {i}: {esc(caption)}"><img src="{image_path}" alt="{esc(alt)}" width="{width}" height="{height}" loading="lazy" decoding="async"></a><figcaption><span class="figure-number">Fig. {i}</span><strong>{esc(caption)}</strong><p class="figure-description">{esc(description)}</p></figcaption></figure>'
publication_gallery += '</div></section>'
publication_gallery += '<dialog class="band-lightbox" aria-label="Research photo and figure viewer"><div class="band-viewer"><button type="button" class="band-close" aria-label="Close photo viewer">Close ×</button><img class="band-full" alt=""><div class="band-controls"><button type="button" class="band-prev" aria-label="Previous photo">← Previous</button><span class="band-count" aria-live="polite"></span><button type="button" class="band-next" aria-label="Next photo">Next →</button></div></div></dialog>'

teaching_gallery = '<section class="internship-gallery-section" aria-labelledby="teaching-gallery-heading"><h2 id="teaching-gallery-heading" class="group-title">Learning by Building</h2><div class="internship-gallery teaching-gallery"><figure class="internship-figure"><a class="band-photo" href="assets/teaching/digital-clock-project.png" target="_blank" rel="noopener noreferrer" aria-label="View digital clock project"><img src="assets/teaching/digital-clock-project.png" alt="digital clock project with a development board, breadboard wiring, and seven-segment displays" width="2048" height="1536" loading="lazy" decoding="async"></a><figcaption><span class="figure-number">Fig. 1</span><strong>Digital Clock Project</strong><p class="figure-description">A hands-on Verilog and DE0-Nano FPGA project used to guide students through digital-logic implementation, hardware testing, and systematic debugging.</p></figcaption></figure><figure class="internship-figure"><a class="band-photo" href="assets/teaching/fpga-programming-tutorial.png" target="_blank" rel="noopener noreferrer" aria-label="View pin assignment and FPGA programming tutorial"><img src="assets/teaching/fpga-programming-tutorial.png" alt="Recorded DE0-Nano tutorial demonstrating pin assignments and FPGA programming in Quartus" width="1913" height="782" loading="lazy" decoding="async"></a><figcaption><span class="figure-number">Fig. 2</span><strong>Pin Assignment &amp; FPGA Programming Tutorial</strong><p class="figure-description">Supplementary instructional material demonstrating pin assignment and FPGA programming for the DE0-Nano laboratory.</p></figcaption></figure></div></section>'
teaching_gallery += '<dialog class="band-lightbox" aria-label="Teaching project photo viewer"><div class="band-viewer"><button type="button" class="band-close" aria-label="Close photo viewer">Close ×</button><img class="band-full" alt=""><div class="band-controls"><button type="button" class="band-prev" aria-label="Previous photo">← Previous</button><span class="band-count" aria-live="polite"></span><button type="button" class="band-next" aria-label="Next photo">Next →</button></div></div></dialog>'

education_gallery = '<section class="internship-gallery-section" aria-labelledby="education-gallery-heading"><h2 id="education-gallery-heading" class="group-title">Exploring the Semiconductor World</h2><div class="internship-gallery"><figure class="internship-figure"><a class="band-photo" href="assets/education/training-01.png" target="_blank" rel="noopener noreferrer" aria-label="View training figure 1"><img src="assets/education/training-01.png" alt="AIT semiconductor collaboration program certificate of completion" width="998" height="702" loading="lazy" decoding="async"></a><figcaption><span class="figure-number">Fig. 1</span><strong>Virtual U.S.–Taiwan–Japan Semiconductor Collaboration Program by AIT</strong><br>Certificate of completion, 2026.</figcaption></figure><figure class="internship-figure"><a class="band-photo" href="assets/education/training-02.png" target="_blank" rel="noopener noreferrer" aria-label="View training figure 2"><img src="assets/education/training-02.png" alt="SEMICON Taiwan 2025 academia participation badge" width="1536" height="2048" loading="lazy" decoding="async"></a><figcaption><span class="figure-number">Fig. 2</span><strong>SEMICON Taiwan 2025</strong><br>A leading exhibition for the global semiconductor industry.</figcaption></figure></div></section><dialog class="band-lightbox" aria-label="Education and training photo viewer"><div class="band-viewer"><button type="button" class="band-close" aria-label="Close photo viewer">Close ×</button><img class="band-full" alt=""><div class="band-controls"><button type="button" class="band-prev" aria-label="Previous photo">← Previous</button><span class="band-count" aria-live="polite"></span><button type="button" class="band-next" aria-label="Next photo">Next →</button></div></div></dialog>'

page_specs = [
    ('about', 'About Me', 'index.html', None, None),
    ('research', 'Research Experience', 'research.html', 'Research experience', research),
    ('publications', 'Publications & Presentations', 'papers.html', 'Publications & Presentations', pubs + publication_gallery),
    ('experience', 'Internships', 'experience.html', 'Internships', experience + internship_gallery),
    ('teaching', 'Teaching & Mentoring', 'teaching.html', 'Teaching & Mentoring', teaching + teaching_gallery),
    ('education', 'Education & Training', 'education.html', 'Education & Training', education + education_gallery),
    ('awards', 'Honors & Awards', 'awards.html', 'Honors & Awards', awards),
    ('leadership', 'Beyond Research', 'beyond-research.html', 'Beyond Research', leadership + personal_gallery + live_band_gallery),
]
sidebar = sidebar.replace('href="#about"', 'href="index.html"')
about = about.replace('href="#publications"', 'href="papers.html"').replace('Explore my research <span aria-hidden="true">↓</span>', 'Explore my research <span aria-hidden="true">↗</span>')
about = about.replace('optimization. In AIoT,', 'optimization.</p><p>In AIoT,')
contact_section = '<section id="contact" class="contact-section"><p class="eyebrow">CONTACT</p><h2>Get in touch</h2><p>For research conversations and PhD opportunities.</p><div class="contact-links">'+contact+'</div></section>'
theme_control = '<label class="theme-control"><span>Theme</span><select aria-label="Color theme" data-theme-picker><option value="light">Light</option><option value="dark">Dark</option></select></label>'
for idx, (key, label, filename, title, content) in enumerate(page_specs):
    navigation = ''.join('<a href="'+f+'"'+(' class="active" aria-current="page"' if k==key else '')+'>'+l.replace(' & ', ' &amp;<br>').replace('Beyond Research', 'Beyond<br>Research').replace('Research Experience', 'Research<br>Experience')+'</a>' for k,l,f,_,_ in page_specs)
    header = '<header class="masthead"><div class="masthead-inner"><a class="wordmark" href="index.html">Chun-Lin Liao (Edward Liao)</a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-navigation">Menu <span aria-hidden="true">☰</span></button><nav id="main-navigation" aria-label="Main navigation">'+navigation+'</nav>'+theme_control+'</div></header>'
    if key == 'about':
        main_content = '<div class="reading-pane">'+about+'</div>'+contact_section
    else:
        page_heading = '<div class="page-heading"><p class="eyebrow">'+f'{idx:02d}'+' / '+label.upper()+'</p><h1>'+title+'</h1></div>'
        main_content = '<div class="reading-pane"><section id="'+key+'" class="topic-section">'+page_heading+content+'</section></div>'
    page_head = head.replace('<title>Chun-Lin Liao | Academic Portfolio</title>', '<title>'+label+' | Chun-Lin Liao</title>')
    if key == 'experience':
        page_head = page_head.replace('</head>', '<link rel="stylesheet" href="assets/internships/gallery.css?v=2"></head>')
    if key == 'publications':
        page_head = page_head.replace('</head>', '<link rel="stylesheet" href="assets/internships/gallery.css?v=1"><link rel="stylesheet" href="assets/publications/gallery.css?v=1"></head>')
    if key == 'teaching':
        page_head = page_head.replace('</head>', '<link rel="stylesheet" href="assets/internships/gallery.css?v=2"><link rel="stylesheet" href="assets/teaching/gallery.css?v=2"></head>')
    if key == 'education':
        page_head = page_head.replace('</head>', '<link rel="stylesheet" href="assets/internships/gallery.css?v=1"></head>')
    if key == 'leadership':
        page_head = page_head.replace('</head>', '<link rel="stylesheet" href="assets/live-band/captions.css?v=4"></head>')
    (D/filename).write_text(page_head+'<body class="portfolio page-'+key+'"><a class="skip-link" href="#main">Skip to content</a>'+header+'<div class="layout">'+sidebar+'<main id="main">'+main_content+footer+'</main></div><script src="assets/site.js?v=3"></script></body></html>', encoding='utf-8')

(D/'cv.html').write_text(head.replace('<title>Chun-Lin Liao | Academic Portfolio</title>','<title>Chun-Lin Liao | Curriculum Vitae</title>')+'<body class="cv-page"><div class="cv-toolbar"><a href="index.html">← Academic portfolio</a><button id="print-cv">Print / save as PDF</button>'+theme_control+'</div><main class="cv-document"><h1>Chun-Lin Liao</h1><p>Mechatronic Engineering · <a href="https://en.ntnu.edu.tw/aboutus.php" target="_blank" rel="noopener noreferrer">National Taiwan Normal University</a><br>Taipei, Taiwan</p><div class="cv-contact">'+contact+'</div><h2>Research interests</h2><p>Trustworthy Agentic AI and AI-Enabled Decision Systems, focusing on evidence-grounded reasoning, explainable and uncertainty-aware decision making, AIoT (Artificial Internet of Things), and real-world AI applications. I integrate AI with connected sensors, embedded systems, and edge devices for monitoring and decision making, with applications in healthcare, public infrastructure, and enterprise workflows.</p>'+sections+'</main><script src="assets/site.js?v=3"></script></body></html>',encoding='utf-8')
(D/'assets'/'site.js').write_text('''const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('#main-navigation');
menuToggle?.addEventListener('click', () => {
  const expanded = menuToggle.getAttribute('aria-expanded') !== 'true';
  menuToggle.setAttribute('aria-expanded', String(expanded));
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuToggle?.getAttribute('aria-expanded') === 'true') {
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.focus();
  }
});
document.querySelector('#print-cv')?.addEventListener('click',()=>window.print());
if(document.body.classList.contains('cv-page')) document.querySelectorAll('details').forEach(d=>d.open=true);
const legacyPages={research:'research.html',publications:'papers.html',experience:'experience.html',teaching:'teaching.html',education:'education.html',awards:'awards.html',leadership:'beyond-research.html'};
if(document.body.classList.contains('page-about') && legacyPages[location.hash.slice(1)]) location.replace(legacyPages[location.hash.slice(1)]);

const bandLinks = [...document.querySelectorAll('.band-photo')];
const bandDialog = document.querySelector('.band-lightbox');
if (bandDialog && typeof bandDialog.showModal === 'function') {
  let bandIndex = 0;
  let bandOpener;
  const fullImage = bandDialog.querySelector('.band-full');
  const count = bandDialog.querySelector('.band-count');
  const showBandPhoto = index => {
    bandIndex = (index + bandLinks.length) % bandLinks.length;
    const source = bandLinks[bandIndex].querySelector('img');
    fullImage.src = bandLinks[bandIndex].href;
    fullImage.alt = source.alt;
    count.textContent = `${bandIndex + 1} / ${bandLinks.length}`;
  };
  bandLinks.forEach((link, index) => link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    bandOpener = link;
    showBandPhoto(index);
    bandDialog.showModal();
    document.documentElement.classList.add('band-viewing');
    bandDialog.querySelector('.band-close').focus();
  }));
  bandDialog.querySelector('.band-close').addEventListener('click', () => bandDialog.close());
  bandDialog.querySelector('.band-prev').addEventListener('click', () => showBandPhoto(bandIndex - 1));
  bandDialog.querySelector('.band-next').addEventListener('click', () => showBandPhoto(bandIndex + 1));
  bandDialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      showBandPhoto(bandIndex + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  bandDialog.addEventListener('click', event => { if (event.target === bandDialog) bandDialog.close(); });
  bandDialog.addEventListener('close', () => {
    document.documentElement.classList.remove('band-viewing');
    bandOpener?.focus({preventScroll:true});
  });
}

''',encoding='utf-8')
(D/'assets'/'favicon.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="title"><title id="title">C.-L. monogram</title><defs><linearGradient id="bg" x1="8" y1="7" x2="56" y2="58" gradientUnits="userSpaceOnUse"><stop stop-color="#102b34"/><stop offset="1" stop-color="#1b5967"/></linearGradient></defs><rect x="2" y="2" width="60" height="60" rx="14" fill="url(#bg)"/><path d="M8 18h7V11h5M44 53h5v-7h7" fill="none" stroke="#65ddd5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="8" cy="18" r="2.4" fill="#65ddd5"/><circle cx="56" cy="46" r="2.4" fill="#f0b46a"/><text x="32" y="40" text-anchor="middle" font-family="Georgia,serif" font-size="22" font-weight="700" letter-spacing="-1.1"><tspan fill="#ffffff">C.</tspan><tspan fill="#65ddd5">-</tspan><tspan fill="#ffffff">L.</tspan></text><path d="M19 47c8 3 18 3 26 0" fill="none" stroke="#f0b46a" stroke-width="1.8" stroke-linecap="round"/></svg>''',encoding='utf-8')
(ROOT/'content.json').write_text(json.dumps({'papers':papers,'courses':courses,'skills':skills},ensure_ascii=False,indent=2),encoding='utf-8')
print('Created portfolio and printable CV with',len(papers),'research entries.')
