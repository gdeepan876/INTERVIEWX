"""
Curated Question Bank for INTERVIEWX.
Provides structured primary questions and contextual follow-up pools
across all 4 roles, 2 interview types, and 3 difficulty levels.
"""

from typing import List, Dict, Any

QUESTION_BANK: Dict[str, Dict[str, Dict[str, List[Dict[str, Any]]]]] = {
    "Java Developer": {
        "Technical": {
            "Beginner": [
                {
                    "text": "What is the difference between '==' and the '.equals()' method in Java when comparing objects and Strings?",
                    "category": "Core Java / Object Equality",
                    "follow_up": "What happens if a class overrides 'equals()' but forgets to override 'hashCode()'?"
                },
                {
                    "text": "Explain the concept of method Overloading vs method Overriding in Java with practical examples.",
                    "category": "Object-Oriented Programming",
                    "follow_up": "Can you override a private or static method in a subclass in Java? Why or why not?"
                },
                {
                    "text": "What is the difference between ArrayList and LinkedList in the Java Collections Framework, and when would you choose one over the other?",
                    "category": "Collections Framework",
                    "follow_up": "How does ArrayList handle resizing internally when its capacity is exceeded?"
                },
                {
                    "text": "How does Exception handling work in Java? Explain the difference between Checked and Unchecked exceptions.",
                    "category": "Error Handling",
                    "follow_up": "Under what circumstance would the 'finally' block NOT execute in Java?"
                },
                {
                    "text": "What is the purpose of the 'final' keyword when applied to a variable, a method, and a class?",
                    "category": "Core Syntax & Immutability",
                    "follow_up": "If a final variable references a List object, can elements still be added to that List?"
                }
            ],
            "Intermediate": [
                {
                    "text": "Explain how Java's Generics work under the hood. What is Type Erasure and what limitations does it impose?",
                    "category": "Generics & Type System",
                    "follow_up": "Why can't you instantiate a generic array directly like 'new T[10]' in Java?"
                },
                {
                    "text": "How does the Java Memory Model organize Heap and Stack memory? What role does Garbage Collection play in managing the Young and Old generations?",
                    "category": "JVM & Memory Management",
                    "follow_up": "What triggers a 'Stop-the-World' garbage collection pause, and how does the G1 collector minimize it?"
                },
                {
                    "text": "Explain thread safety in Java. How does 'ConcurrentHashMap' achieve concurrency without locking the entire map like 'Hashtable' does?",
                    "category": "Concurrency & Multithreading",
                    "follow_up": "What is the difference between the 'volatile' keyword and a 'synchronized' block?"
                },
                {
                    "text": "In Spring Boot, how does Dependency Injection work and what is the difference between '@Component', '@Service', and '@Repository'?",
                    "category": "Spring Boot & IoC",
                    "follow_up": "What are the common Spring Bean scopes, and why is injecting a Request-scoped bean into a Singleton-scoped bean tricky?"
                },
                {
                    "text": "What is the N+1 select problem in JPA/Hibernate, and what specific strategies do you use to detect and eliminate it?",
                    "category": "JPA / Database ORM",
                    "follow_up": "What is the difference between JOIN FETCH and using an EntityGraph?"
                }
            ],
            "Advanced": [
                {
                    "text": "Describe the internal architecture of the JVM Garbage Collectors (e.g., G1 vs ZGC). How does ZGC achieve sub-millisecond maximum pause times?",
                    "category": "Advanced JVM Internals",
                    "follow_up": "How do colored pointers and load barriers function together in ZGC during concurrent compaction?"
                },
                {
                    "text": "How do you design a distributed transaction strategy across microservices in Spring Boot? Compare the Saga Pattern (choreography vs orchestration) with Two-Phase Commit (2PC).",
                    "category": "Distributed Architecture",
                    "follow_up": "In an orchestrated Saga, how do you guarantee idempotent compensation if a compensating transaction fails halfway?"
                },
                {
                    "text": "Analyze the concurrency mechanisms introduced in Java 21 Virtual Threads (Project Loom). How do they fundamentally change thread-per-request models?",
                    "category": "High Concurrency & Project Loom",
                    "follow_up": "What is 'carrier thread pinning', and what legacy Java constructs cause virtual threads to get pinned?"
                },
                {
                    "text": "Explain classloader hierarchy in the JVM. How does classloader isolation work in modular frameworks like OSGi or application servers?",
                    "category": "JVM Classloading & Security",
                    "follow_up": "How does the parent-first delegation model prevent core Java classes from being overridden by malicious bytecode?"
                },
                {
                    "text": "How would you architect a zero-downtime, high-throughput financial transaction processing engine handling 50,000 TPS using Java?",
                    "category": "High-Throughput System Design",
                    "follow_up": "How would the LMAX Disruptor pattern or ring buffers outperform traditional Java blocking queues in this scenario?"
                }
            ]
        },
        "HR": {
            "Beginner": [
                {
                    "text": "Tell me about yourself, your background in software engineering, and why you are interested in a Java Developer position.",
                    "category": "Introduction & Motivation",
                    "follow_up": "What was the most challenging project you worked on during your studies or early work, and what did you learn?"
                },
                {
                    "text": "Describe a situation where you had to learn a new framework or technology quickly. How did you approach the learning curve?",
                    "category": "Adaptability & Learning",
                    "follow_up": "If you got stuck while learning it, what resources or steps did you take before asking for help?"
                },
                {
                    "text": "How do you prioritize your daily tasks when you have multiple assignments due around the same time?",
                    "category": "Time Management",
                    "follow_up": "What do you do if you realize you might miss a deadline?"
                },
                {
                    "text": "Give an example of a time you received constructive criticism on your code during a review. How did you react?",
                    "category": "Feedback & Growth Mindset",
                    "follow_up": "Did you agree with the feedback initially, and how did you resolve any differing opinions?"
                },
                {
                    "text": "Where do you see yourself professionally in the next two to three years?",
                    "category": "Career Aspirations",
                    "follow_up": "What specific technical or leadership skills are you most eager to build during that timeframe?"
                }
            ],
            "Intermediate": [
                {
                    "text": "Describe a time when you and a senior colleague or product manager had a technical disagreement regarding an implementation. How did you navigate it?",
                    "category": "Conflict Resolution & Alignment",
                    "follow_up": "What data or benchmarks did you bring to support your viewpoint?"
                },
                {
                    "text": "Can you share an experience where a critical production bug occurred in your application? Walk me through your troubleshooting process and communication.",
                    "category": "Crisis Management & Ownership",
                    "follow_up": "How did you ensure a post-mortem was conducted and that the root cause was permanently addressed?"
                },
                {
                    "text": "How do you balance writing pristine, maintainable code with meeting demanding business deadlines?",
                    "category": "Engineering Pragmatism",
                    "follow_up": "How do you track and advocate for resolving accumulated technical debt with non-technical stakeholders?"
                },
                {
                    "text": "Tell me about a time you mentored a junior engineer or helped an intern onboard onto your codebase.",
                    "category": "Mentorship & Team Collaboration",
                    "follow_up": "How did you adapt your mentoring style to their particular learning pace?"
                },
                {
                    "text": "Why do you feel this role is the natural next step in your career journey compared to your current position?",
                    "category": "Role Motivation & Alignment",
                    "follow_up": "What unique perspective or strength would you bring to our existing engineering team?"
                }
            ],
            "Advanced": [
                {
                    "text": "As a senior engineer, how do you drive consensus on major architectural decisions across multiple independent teams?",
                    "category": "Technical Leadership & Consensus",
                    "follow_up": "How do you handle a scenario where an engineering team strongly opposes an architecture mandate from your group?"
                },
                {
                    "text": "Describe a time when an engineering project you spearheaded failed to meet its objective or had to be canceled. What happened and what were the takeaways?",
                    "category": "Resilience & Accountability",
                    "follow_up": "How did you maintain team morale and trust with executive leadership following that cancellation?"
                },
                {
                    "text": "How do you cultivate a healthy engineering culture focused on psychological safety, continuous learning, and high code quality?",
                    "category": "Culture & Team Health",
                    "follow_up": "What specific metrics or signals do you look at to detect early symptoms of burnout among team members?"
                },
                {
                    "text": "Give an example of how you translated complex technical constraints into clear business risks and opportunities for executive leadership.",
                    "category": "Executive Communication",
                    "follow_up": "How did the executive team's decision impact your subsequent architectural roadmap?"
                },
                {
                    "text": "What is your philosophy on hiring and building high-performing engineering teams?",
                    "category": "Hiring & Talent Strategy",
                    "follow_up": "How do you assess cultural adaptability and problem-solving grit beyond raw technical syntax in interviews?"
                }
            ]
        }
    },
    "Python Developer": {
        "Technical": {
            "Beginner": [
                {
                    "text": "What is the difference between mutable and immutable data types in Python? Give two examples of each.",
                    "category": "Core Python Fundamentals",
                    "follow_up": "Why is it dangerous to use a mutable default argument like 'def func(items=[])'?"
                },
                {
                    "text": "Explain how list comprehensions work in Python and how they compare to traditional 'for' loops in terms of readability and execution speed.",
                    "category": "Pythonic Idioms",
                    "follow_up": "When would you prefer a generator expression '(x for x in data)' over a list comprehension '[x for x in data]'?"
                },
                {
                    "text": "What are *args and **kwargs in Python function definitions, and how do they allow flexible argument passing?",
                    "category": "Functions & Parameters",
                    "follow_up": "Can you have positional arguments after *args in Python 3? What are they called?"
                },
                {
                    "text": "How does Python handle memory management and garbage collection? Mention reference counting and circular references.",
                    "category": "Memory Management",
                    "follow_up": "How does the 'gc' module detect cyclic references that reference counting cannot resolve?"
                },
                {
                    "text": "What is the difference between 'is' and '==' in Python?",
                    "category": "Comparison Operators",
                    "follow_up": "Why does 'a = 256; b = 256; a is b' return True, but 'a = 1000; b = 1000; a is b' might return False in an interactive session?"
                }
            ],
            "Intermediate": [
                {
                    "text": "Explain Python Decorators. How do they work under the hood using closures, and how would you write a decorator that accepts arguments?",
                    "category": "Decorators & Metaprogramming",
                    "follow_up": "Why is 'functools.wraps' important when writing production decorators?"
                },
                {
                    "text": "What is the Global Interpreter Lock (GIL) in CPython, and how does it impact multi-threaded CPU-bound vs I/O-bound tasks?",
                    "category": "CPython Internals & Concurrency",
                    "follow_up": "What is the difference between using the 'threading' module and the 'multiprocessing' module to bypass the GIL?"
                },
                {
                    "text": "How does Python's 'asyncio' event loop work? Explain the difference between 'async def', 'await', and running synchronous blocking code.",
                    "category": "Asynchronous Programming",
                    "follow_up": "What happens if someone puts a blocking call like 'time.sleep()' or a synchronous database query inside an async route handler in FastAPI?"
                },
                {
                    "text": "Explain how Python Generators and the 'yield' keyword function. What makes them memory efficient when processing large datasets?",
                    "category": "Generators & Iteration",
                    "follow_up": "What is the purpose of 'yield from' in Python?"
                },
                {
                    "text": "In FastAPI or Django, how do you handle database connection pooling and manage transactions safely in asynchronous contexts?",
                    "category": "Frameworks & Databases",
                    "follow_up": "How does dependency injection in FastAPI ('Depends') help with session lifecycle management?"
                }
            ],
            "Advanced": [
                {
                    "text": "Explain Python Metaclasses. How does '__init_subclass__' or 'type' subclassing alter class creation, and what is a legitimate production use case?",
                    "category": "Advanced Metaprogramming",
                    "follow_up": "How do libraries like Pydantic or SQLAlchemy utilize metaclasses to generate schema validators dynamically?"
                },
                {
                    "text": "Analyze the free-threaded Python build (PEP 703 - removing the GIL) in modern CPython. What are the memory synchronization trade-offs?",
                    "category": "CPython Evolution & Memory",
                    "follow_up": "How does mimalloc integration and biased reference counting mitigate performance regressions in single-threaded code?"
                },
                {
                    "text": "How would you design a distributed asynchronous task queue in Python (similar to Celery or Dramatiq) from scratch using Redis as a broker?",
                    "category": "Distributed Systems & Queues",
                    "follow_up": "How would you guarantee at-least-once message delivery while handling worker crash failures and poison pills?"
                },
                {
                    "text": "How do Python descriptors work ('__get__', '__set__', '__delete__')? Differentiate between data descriptors and non-data descriptors.",
                    "category": "Object Model & Descriptors",
                    "follow_up": "How does the '@property' decorator leverage descriptors under the hood?"
                },
                {
                    "text": "How do you profile, identify, and resolve a memory leak in a high-volume long-running Python service?",
                    "category": "Performance & Debugging",
                    "follow_up": "Which tools (tracemalloc, objgraph, py-spy, memray) would you deploy and what signals would you look for?"
                }
            ]
        },
        "HR": {
            "Beginner": [
                {
                    "text": "Why did you choose Python as your primary programming language, and what types of applications do you enjoy building most?",
                    "category": "Motivation & Background",
                    "follow_up": "What do you consider the biggest strength and the biggest limitation of Python?"
                },
                {
                    "text": "Describe a project where you collaborated with a team member using Git. How did you resolve merge conflicts or code review notes?",
                    "category": "Team Collaboration & Git",
                    "follow_up": "What branch management strategy (e.g. GitHub Flow, Gitflow) did you adopt?"
                },
                {
                    "text": "How do you test your Python code before submitting a pull request? What testing libraries have you used?",
                    "category": "Code Quality & Testing",
                    "follow_up": "Have you used pytest fixtures or mock objects in your tests?"
                },
                {
                    "text": "Can you describe a time when you struggled to solve a stubborn bug and how you overcame the frustration?",
                    "category": "Problem Solving & Persistence",
                    "follow_up": "What step in your debugging process finally helped you identify the issue?"
                },
                {
                    "text": "What do you hope to achieve in your first 90 days if you join our team?",
                    "category": "Onboarding & Goals",
                    "follow_up": "How would you measure your own success during that onboarding window?"
                }
            ],
            "Intermediate": [
                {
                    "text": "Tell me about a time you identified a major performance bottleneck in a Python codebase. How did you advocate for refactoring it?",
                    "category": "Engineering Ownership",
                    "follow_up": "How did you prove the performance improvement to stakeholders with benchmarks?"
                },
                {
                    "text": "Describe an instance where you had to push back against an unrealistic project deadline. How did you negotiate scope?",
                    "category": "Stakeholder Negotiation",
                    "follow_up": "What features did you recommend deferring to a subsequent release?"
                },
                {
                    "text": "How do you establish code review standards within a Python development team to avoid subjective bike-shedding?",
                    "category": "Code Review Best Practices",
                    "follow_up": "How do you leverage linters (Ruff, Black, Flake8, Mypy) to automate routine stylistic checks?"
                },
                {
                    "text": "Share an experience where a requirements change occurred halfway through a sprint. How did you adapt your architecture?",
                    "category": "Agility & Adaptability",
                    "follow_up": "How did you ensure that existing unit tests stayed relevant?"
                },
                {
                    "text": "What motivates you most in your daily engineering work, and what work environments bring out your best performance?",
                    "category": "Workplace Culture",
                    "follow_up": "How do you maintain high productivity in a hybrid or remote setup?"
                }
            ],
            "Advanced": [
                {
                    "text": "How do you mentor engineers to write idiomatic, maintainable Python rather than treating Python like Java or C++?",
                    "category": "Engineering Leadership",
                    "follow_up": "What are the most common anti-patterns you observe mid-level developers bring into Python codebases?"
                },
                {
                    "text": "Tell me about a high-stakes technical decision you made that had multi-year architectural implications for your company.",
                    "category": "Strategic Architecture",
                    "follow_up": "In hindsight, is there anything you would have structured differently?"
                },
                {
                    "text": "How do you handle a team member who consistently writes fragile code or resists adopting modern testing and CI/CD standards?",
                    "category": "Performance Coaching",
                    "follow_up": "What timeline and checkpoints do you set for measurable improvement?"
                },
                {
                    "text": "Describe how you have contributed to open-source communities, tech talks, or cross-organizational knowledge sharing.",
                    "category": "Community & Influence",
                    "follow_up": "How has contributing to open source influenced your day-to-day software design habits?"
                },
                {
                    "text": "What principles guide your approach to legacy system migration when replacing a monolithic Python service?",
                    "category": "System Modernization",
                    "follow_up": "How do you manage database schema migrations with zero customer-facing downtime?"
                }
            ]
        }
    },
    "Frontend Developer": {
        "Technical": {
            "Beginner": [
                {
                    "text": "Explain the Box Model in CSS. How do 'content-box' and 'border-box' differ when sizing an element?",
                    "category": "HTML & CSS Core",
                    "follow_up": "Why is 'box-sizing: border-box' almost universally set on the root selector in modern CSS resets?"
                },
                {
                    "text": "What is the difference between 'var', 'let', and 'const' in JavaScript? Explain the concepts of scope and hoisting.",
                    "category": "Modern JavaScript (ES6+)",
                    "follow_up": "Can you reassign properties of an object declared with 'const'? Why?"
                },
                {
                    "text": "What is the Virtual DOM in React, and how does React's reconciliation process optimize DOM updates?",
                    "category": "React Fundamentals",
                    "follow_up": "Why is using array index as a 'key' prop in React lists considered an anti-pattern when items can be reordered?"
                },
                {
                    "text": "Explain the purpose of the 'useState' and 'useEffect' hooks in React with practical use cases.",
                    "category": "React Hooks",
                    "follow_up": "What causes an infinite re-render loop inside a 'useEffect' hook, and how do you prevent it?"
                },
                {
                    "text": "How do CSS Flexbox and CSS Grid differ, and when would you choose Flexbox over Grid?",
                    "category": "CSS Layouts",
                    "follow_up": "How do you center an element both vertically and horizontally using Flexbox?"
                }
            ],
            "Intermediate": [
                {
                    "text": "Explain the JavaScript Event Loop. How do the Call Stack, Macro-task Queue (Task Queue), and Micro-task Queue (Promises) interact?",
                    "category": "JavaScript Runtime & Async",
                    "follow_up": "In what exact order will 'console.log(1)', 'setTimeout(() => console.log(2), 0)', and 'Promise.resolve().then(() => console.log(3))' execute?"
                },
                {
                    "text": "How does React manage component re-renders? When and how should you utilize 'useMemo', 'useCallback', and 'React.memo' to avoid premature optimization?",
                    "category": "React Performance",
                    "follow_up": "What is the computational cost of wrapping every single callback in 'useCallback' indiscriminately?"
                },
                {
                    "text": "Compare state management approaches in React: Context API vs External stores (such as Zustand, Redux Toolkit). When does Context cause performance degradation?",
                    "category": "State Management Architecture",
                    "follow_up": "Why does updating a Context value cause all consumer components to re-render, and how can you isolate updates?"
                },
                {
                    "text": "How do you audit and improve Web Vitals (Largest Contentful Paint - LCP, Cumulative Layout Shift - CLS, Interaction to Next Paint - INP)?",
                    "category": "Web Performance & Core Vitals",
                    "follow_up": "What are common frontend causes of high CLS, and how does setting aspect ratios on image containers fix it?"
                },
                {
                    "text": "What strategies do you implement to ensure web accessibility (a11y) compliant with WCAG 2.1 AA standards?",
                    "category": "Web Accessibility (a11y)",
                    "follow_up": "How do ARIA live regions assist screen reader users during dynamic single-page app content updates?"
                }
            ],
            "Advanced": [
                {
                    "text": "Analyze the architectural differences between React Server Components (RSC) and traditional Client-Side Hydration. How does RSC impact the client bundle footprint?",
                    "category": "Modern Rendering Architecture",
                    "follow_up": "How do Server Actions work under the hood, and how do they manage serialization between the Node server and the client browser?"
                },
                {
                    "text": "How would you architect a Micro-Frontend architecture for an enterprise web platform? Compare Module Federation with iframe or web-component based solutions.",
                    "category": "Micro-Frontends & System Design",
                    "follow_up": "How do you handle shared dependencies (like React runtime) to avoid loading multiple duplicated bundles across micro-apps?"
                },
                {
                    "text": "Describe your strategy for code-splitting, tree-shaking, and bundle size optimization using modern bundlers (Vite / Rollup / Webpack).",
                    "category": "Build Tooling & Optimization",
                    "follow_up": "Why does importing a single icon from a barrel file 'import { Icon } from 'icons'' often blow up bundle sizes if sideEffects aren't configured?"
                },
                {
                    "text": "How do you build a resilient offline-first Single Page Application with Service Workers, IndexedDB, and background synchronization?",
                    "category": "Progressive Web Apps & Offline",
                    "follow_up": "How do you resolve conflict when data modified offline clashes with server data upon reconnection?"
                },
                {
                    "text": "How would you design a production Design System component library with automated visual regression testing and tokens?",
                    "category": "Design Systems & Tooling",
                    "follow_up": "How do you balance CSS-in-JS, Tailwind CSS, or vanilla CSS Modules for maximum performance and design token flexibility?"
                }
            ]
        },
        "HR": {
            "Beginner": [
                {
                    "text": "What inspired you to pursue frontend development, and what is your favorite web application from an interaction design perspective?",
                    "category": "Passion & UX Sensibility",
                    "follow_up": "What specific UI details in that application make it feel so intuitive to you?"
                },
                {
                    "text": "How do you collaborate with UI/UX designers when a mock-up contains edge cases or interactions that are technically difficult to implement?",
                    "category": "Design Collaboration",
                    "follow_up": "Can you give an example where you suggested an alternative design that preserved user experience while reducing build complexity?"
                },
                {
                    "text": "How do you test and verify your user interfaces across multiple browsers, operating systems, and device screen sizes?",
                    "category": "Cross-Platform Empathy",
                    "follow_up": "Have you ever encountered a layout bug that only reproduced on Mobile Safari, and how did you resolve it?"
                },
                {
                    "text": "Tell me about a time you received critical feedback from a user or QA tester regarding an interface you built. How did you handle it?",
                    "category": "User Focus & Quality",
                    "follow_up": "How did you translate that feedback into actionable engineering tickets?"
                },
                {
                    "text": "How do you keep up with the rapidly shifting JavaScript and frontend ecosystem without feeling overwhelmed?",
                    "category": "Continuous Learning",
                    "follow_up": "What is one recent frontend feature or pattern you adopted after reading about it?"
                }
            ],
            "Intermediate": [
                {
                    "text": "Describe a scenario where marketing or product demanded a new feature launch on short notice, requiring UI trade-offs. How did you manage expectations?",
                    "category": "Product Delivery & Trade-offs",
                    "follow_up": "How did you ensure that accessibility and performance were not sacrificed for speed?"
                },
                {
                    "text": "Can you share a time when you noticed a user experience flaw that wasn't caught in the product specs? How did you champion fixing it?",
                    "category": "Product Sense & Initiative",
                    "follow_up": "What qualitative or quantitative metrics did you use to validate the improvement?"
                },
                {
                    "text": "How do you maintain empathy and effective communication with backend engineers who may have different mental models of API contracts?",
                    "category": "Frontend-Backend Alignment",
                    "follow_up": "How do you establish early API contracts or mock servers to unblock parallel development?"
                },
                {
                    "text": "Tell me about a time you improved the developer experience (DX) or build pipeline for your frontend team.",
                    "category": "Developer Experience",
                    "follow_up": "How much build time or onboarding friction did that improvement eliminate?"
                },
                {
                    "text": "What qualities do you value most in a technical team leader?",
                    "category": "Leadership Preferences",
                    "follow_up": "How do you prefer to receive feedback on your performance?"
                }
            ],
            "Advanced": [
                {
                    "text": "How do you advocate for and justify technical investments in frontend infrastructure (like migrating to TypeScript or rebuilding a design system) to non-technical executives?",
                    "category": "Executive Advocacy & ROI",
                    "follow_up": "What financial or velocity metrics did you present to show business return?"
                },
                {
                    "text": "Describe your methodology for conducting frontend architectural reviews across multiple product squads.",
                    "category": "Governance & Architecture",
                    "follow_up": "How do you avoid becoming an engineering bottleneck while maintaining platform consistency?"
                },
                {
                    "text": "How do you handle a scenario where product analytics show a 20% drop-off on a newly redesigned checkout flow?",
                    "category": "Incident Diagnosis & Product Empathy",
                    "follow_up": "How do you coordinate with product managers and data analysts to isolate whether the issue is technical or behavioral?"
                },
                {
                    "text": "What is your approach to growing junior and mid-level frontend engineers into high-impact technical leaders?",
                    "category": "Talent Development",
                    "follow_up": "How do you encourage engineers to build empathy for accessibility and internationalization?"
                },
                {
                    "text": "How do you foresee the role of frontend engineering shifting over the next 5 years with AI-assisted code generation?",
                    "category": "Industry Vision",
                    "follow_up": "Which core engineering skills will become more valuable as routine boilerplate generation is automated?"
                }
            ]
        }
    },
    "Backend Developer": {
        "Technical": {
            "Beginner": [
                {
                    "text": "What is the difference between HTTP GET, POST, PUT, PATCH, and DELETE methods? Explain idempotency.",
                    "category": "HTTP & REST Fundamentals",
                    "follow_up": "Which of these methods are considered idempotent, and why is POST typically non-idempotent?"
                },
                {
                    "text": "Explain the difference between SQL (Relational) and NoSQL (Document/Key-Value) databases, and when would you use each?",
                    "category": "Databases & Storage",
                    "follow_up": "What does ACID stand for in relational databases?"
                },
                {
                    "text": "What is an index in a database, and how does it speed up queries? Are there any downsides to adding too many indexes?",
                    "category": "Database Indexing",
                    "follow_up": "How does a B-Tree index structure locate a record in logarithmic time?"
                },
                {
                    "text": "How does authentication differ from authorization? Give an example of how you implement both in a backend API.",
                    "category": "Security & Auth",
                    "follow_up": "What information is typically stored in the payload of a JWT, and why shouldn't sensitive secrets like passwords be included?"
                },
                {
                    "text": "What are HTTP status codes 200, 201, 400, 401, 403, 404, and 500, and when should each be returned?",
                    "category": "API Design Standards",
                    "follow_up": "What is the exact semantic difference between 401 Unauthorized and 403 Forbidden?"
                }
            ],
            "Intermediate": [
                {
                    "text": "Explain database transaction isolation levels (Read Uncommitted, Read Committed, Repeatable Read, Serializable). What anomalies do they protect against?",
                    "category": "Database Concurrency & Isolation",
                    "follow_up": "What is a 'phantom read', and which isolation level prevents it?"
                },
                {
                    "text": "How do you design a caching strategy using Redis? Explain cache-aside, write-through, and cache stampede (thundering herd) mitigation.",
                    "category": "Caching & Redis",
                    "follow_up": "How do TTL jitter or mutex locks prevent a cache stampede when a popular key expires?"
                },
                {
                    "text": "Compare horizontal scaling vs vertical scaling. What architectural considerations must be addressed before running a backend stateless horizontally?",
                    "category": "Scalability & Architecture",
                    "follow_up": "How do you manage user sessions across multiple stateless server instances?"
                },
                {
                    "text": "How do asynchronous message brokers (e.g. RabbitMQ, Kafka) decouple services in a backend architecture?",
                    "category": "Event-Driven Architecture",
                    "follow_up": "What is the difference between a work queue (point-to-point) and a publish-subscribe topic?"
                },
                {
                    "text": "How do rate limiters work in backend APIs? Explain token bucket vs sliding window counter algorithms.",
                    "category": "API Gateway & Resilience",
                    "follow_up": "How would you implement a distributed rate limiter across multiple API gateway nodes using Redis?"
                }
            ],
            "Advanced": [
                {
                    "text": "Explain the CAP Theorem and PACELC theorem. How do you evaluate trade-offs between consistency and availability in a globally distributed system?",
                    "category": "Distributed Systems Theory",
                    "follow_up": "Under PACELC, how does DynamoDB or Cassandra behave in the absence of a network partition?"
                },
                {
                    "text": "How would you design a distributed ID generator (like Twitter Snowflake) that generates 64-bit unique, k-sorted IDs with zero coordination between nodes?",
                    "category": "System Design & Algorithms",
                    "follow_up": "How do you handle clock drift or backward NTP clock adjustments on worker nodes?"
                },
                {
                    "text": "Describe how database sharding works. Compare range-based, hash-based, and directory-based sharding, and explain how to handle re-sharding without downtime.",
                    "category": "Database Sharding & Partitioning",
                    "follow_up": "How does consistent hashing minimize the percentage of keys that must be moved when a new shard is added?"
                },
                {
                    "text": "How do you achieve exactly-once processing semantics in a distributed streaming pipeline using Kafka?",
                    "category": "Event Streaming & Reliability",
                    "follow_up": "What role do idempotent producers and transactional consumer-producer offsets play in Kafka transactions?"
                },
                {
                    "text": "How do you implement zero-downtime database schema migrations for tables containing billions of rows in production?",
                    "category": "Production Operations & DB Migrations",
                    "follow_up": "Walk me through the Expand and Contract (Parallel Run) pattern for renaming or restructuring a column."
                }
            ]
        },
        "HR": {
            "Beginner": [
                {
                    "text": "What drew you to backend engineering rather than frontend or mobile development?",
                    "category": "Career Motivation",
                    "follow_up": "What aspect of backend development gives you the greatest sense of accomplishment?"
                },
                {
                    "text": "Can you describe a time when you collaborated with a frontend engineer or mobile developer to design an API? How did you agree on the contract?",
                    "category": "Cross-Functional Collaboration",
                    "follow_up": "What documentation tools (like Swagger / OpenAPI) did you use to keep the team aligned?"
                },
                {
                    "text": "How do you approach debugging when an API endpoint works perfectly on your local machine but returns errors in the staging environment?",
                    "category": "Troubleshooting & Environment",
                    "follow_up": "What server logs and environment variables do you verify first?"
                },
                {
                    "text": "Describe a project where you had to adhere to strict security or data validation guidelines.",
                    "category": "Security Awareness",
                    "follow_up": "How did you prevent SQL injection and cross-site scripting vulnerabilities?"
                },
                {
                    "text": "What steps do you take when you feel overwhelmed by a complex codebase with minimal documentation?",
                    "category": "Adaptability & Resourcefulness",
                    "follow_up": "How do you contribute back to the documentation once you figure things out?"
                }
            ],
            "Intermediate": [
                {
                    "text": "Tell me about an instance where an API you designed caused unexpected performance degradation in production. How did you handle the situation?",
                    "category": "Accountability & Crisis Response",
                    "follow_up": "What automated alerts or monitoring tools helped you detect the incident?"
                },
                {
                    "text": "How do you balance adding new product features with writing comprehensive automated unit and integration tests?",
                    "category": "Engineering Discipline",
                    "follow_up": "What test coverage percentage or test pyramid philosophy do you aim for?"
                },
                {
                    "text": "Describe a time when you had to convince a product manager that a proposed database schema would not scale. How did you communicate the trade-offs?",
                    "category": "Technical Communication",
                    "follow_up": "What compromise did you propose to meet the business deadline safely?"
                },
                {
                    "text": "How do you conduct code reviews to catch concurrency bugs, security oversights, and unindexed database queries?",
                    "category": "Code Review Vigilance",
                    "follow_up": "How do you give feedback without sounding overly critical or pedantic?"
                },
                {
                    "text": "Where do you want to grow technically over the next two years? What backend architectural patterns are you exploring?",
                    "category": "Professional Growth",
                    "follow_up": "Have you built any side projects or experiments to test those patterns?"
                }
            ],
            "Advanced": [
                {
                    "text": "Describe how you led the response to a Sev-1 production outage affecting core database clusters. How did you communicate with stakeholders during the incident?",
                    "category": "Incident Command & Executive Presence",
                    "follow_up": "How did you run the blameless post-mortem and ensure prevention measures were funded?"
                },
                {
                    "text": "How do you balance the trade-offs between Microservices and Monolithic architectures for an early-stage vs mature engineering organization?",
                    "category": "Architectural Strategy",
                    "follow_up": "What organizational indicators signal that it is genuinely time to decompose a monolith?"
                },
                {
                    "text": "How do you build a culture of security, compliance (SOC2/GDPR/HIPAA), and high reliability across backend engineering teams?",
                    "category": "Governance & Compliance",
                    "follow_up": "How do you ensure security policies don't choke developer deployment velocity?"
                },
                {
                    "text": "Tell me about a time you had to decommission a legacy backend system that was deeply embedded across company workflows.",
                    "category": "Legacy Modernization",
                    "follow_up": "How did you ensure zero data loss and verify parity between old and new systems?"
                },
                {
                    "text": "What is your philosophy on technical debt: when is it strategic, and when does it become existential for a business?",
                    "category": "Strategic Engineering",
                    "follow_up": "How do you allocate sprint capacity (e.g., 80/20 rule) to keep technical debt under control?"
                }
            ]
        }
    }
}


def get_curated_questions(role: str, interview_type: str, difficulty: str) -> List[Dict[str, Any]]:
    """
    Safely retrieves the pool of curated questions for a given role, type, and difficulty.
    Falls back gracefully if an unexpected key is passed.
    """
    try:
        return QUESTION_BANK[role][interview_type][difficulty]
    except KeyError:
        # Fallback to standard Java Developer / Technical / Beginner
        return QUESTION_BANK["Java Developer"]["Technical"]["Beginner"]

