<!-- code2docs:start --># nlp2cmd

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.10-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-3753-green)
> **3753** functions | **713** classes | **935** files | CC̄ = 5.2

> Auto-generated project documentation from source code analysis.

**Author:** NLP2CMD Team  
**License:** Apache-2.0[(LICENSE)](./LICENSE)  
**Repository:** [https://github.com/wronai/nlp2cmd](https://github.com/wronai/nlp2cmd)

## Installation

### From PyPI

```bash
pip install nlp2cmd
```

### From Source

```bash
git clone https://github.com/wronai/nlp2cmd
cd nlp2cmd
pip install -e .
```

### Optional Extras

```bash
pip install nlp2cmd[service]    # service features
pip install nlp2cmd[nlp]    # nlp features
pip install nlp2cmd[llm]    # LLM integration (litellm)
pip install nlp2cmd[router]    # router features
pip install nlp2cmd[sql]    # sql features
pip install nlp2cmd[thermodynamic]    # thermodynamic features
pip install nlp2cmd[browser]    # browser features
pip install nlp2cmd[desktop]    # desktop features
pip install nlp2cmd[automation]    # automation features
pip install nlp2cmd[llm-vision]    # llm-vision features
pip install nlp2cmd[dev]    # development tools
pip install nlp2cmd[all]    # all optional features
```

## Quick Start

### CLI Usage

```bash
# Generate full documentation for your project
nlp2cmd ./my-project

# Only regenerate README
nlp2cmd ./my-project --readme-only

# Preview what would be generated (no file writes)
nlp2cmd ./my-project --dry-run

# Check documentation health
nlp2cmd check ./my-project

# Sync — regenerate only changed modules
nlp2cmd sync ./my-project
```

### Python API

```python
from nlp2cmd import generate_readme, generate_docs, Code2DocsConfig

# Quick: generate README
generate_readme("./my-project")

# Full: generate all documentation
config = Code2DocsConfig(project_name="mylib", verbose=True)
docs = generate_docs("./my-project", config=config)
```




## Architecture

```
nlp2cmd/
├── run_test
├── CONTRIBUTING
├── out_call_graph
├── generate_quick
├── test_nlp2cmd_enhanced
├── oferteo_pl_data
├── goal
├── generate_working
├── test_nlp2cmd_commands
├── install_vnc
    ├── llm
├── out_interprocedural_decision_paths
├── manual_appspec
├── code2llm_workaround
├── requirements-minimal
├── planfile
    ├── markdownlint
├── run_all_tests
├── Makefile
├── config
├── docker-compose
├── THERMODYNAMIC_ARCHITECTURE
├── pyqual
├── requirements
├── requirements-enhanced
├── generated_appspec
├── pyproject
├── tree
├── generate_chunks
├── REPO_SPLIT
├── requirements-thermodynamic
├── pytest
├── projektor
├── TODO
├── examples
├── jspaint_app_test4
├── Dockerfile
├── prefact
├── CHANGELOG
├── out_function_entries
├── THERMODYNAMIC_INTEGRATION
├── project
├── INSTALLATION
├── README
    ├── SCHEMA_VALIDATION_REPORT
    ├── README
        ├── SCHEMA_CONSOLIDATION_SUMMARY
        ├── PROJECT_HISTORY
        ├── TEST_SCRIPTS_README
        ├── TODO
        ├── IMPROVEMENTS
        ├── README
        ├── thermodynamic-computing
        ├── KEYWORD_DETECTION_FLOW
        ├── CANVAS_DRAWING
        ├── web-automation
        ├── DESKTOP_GUI_AUTOMATION
        ├── schema-system
        ├── FIREFOX_SESSION_INJECTION
        ├── BENCHMARKING
        ├── STREAM_PROTOCOLS
        ├── SERVICE_MODE
        ├── README
        ├── user-guide
        ├── python-api
        ├── cli-reference
        ├── examples-guide
    ├── index
    ├── nginx
    ├── docker
        ├── appspec
        ├── sensors
        ├── pip
        ├── openssl
        ├── zip
        ├── cp
        ├── git
        ├── find
        ├── sed
        ├── ls
        ├── kubectl
        ├── gpg
        ├── black
        ├── jq
        ├── python3
        ├── cat
        ├── iconv
        ├── split
        ├── ps
        ├── mv
        ├── nslookup
        ├── rsync
        ├── traceroute
        ├── eslint
        ├── psql
        ├── make
        ├── lsof
        ├── df
        ├── grep
        ├── docker
        ├── sort
        ├── pytest
        ├── chmod
        ├── nmap
        ├── tar
        ├── node
        ├── free
        ├── iptables
            ├── appspec
        ├── mysqldump
        ├── mysql
        ├── npm
        ├── ssh-keygen
        ├── mongodump
        ├── rm
            ├── appspec
        ├── netstat
        ├── uptime
        ├── generated_schemas
        ├── all_schemas
        ├── validated_schemas
            ├── batch_3_final
            ├── quick_batch_2_llm
            ├── batch_3_test
            ├── batch_1_detailed
            ├── batch_2_test
            ├── quick_batch_3_llm
            ├── batch_1_test
            ├── quick_batch_1_llm
            ├── generated_docker_dynamic_schema
            ├── generated_kubectl_dynamic_schema
        ├── linux_shortcuts
        ├── windows_shortcuts
        ├── macos_shortcuts
        ├── open_url
        ├── type_text
        ├── search
        ├── navigate
        ├── click
    ├── show_metrics
    ├── _dynamic_orchestrator
    ├── MAKEFILE_PROSTY
    ├── Makefile
    ├── _example_helpers
    ├── _verbose_helper
    ├── demo_screenshot_video
    ├── README_NLP2CMD
    ├── run_examples
    ├── run_task
    ├── README
        ├── README
            ├── example
            ├── README
            ├── manual_appspec
            ├── end_to_end_demo
            ├── mvp
                ├── run
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
            ├── simple_schema_demo
            ├── demo_intelligent_nlp2cmd
            ├── demo_persistent_storage
            ├── demo_enhanced
            ├── demo_schema_flow
            ├── demo_version_detection
            ├── schema_flow_demo
            ├── example
            ├── README
        ├── 01_diagnose_credentials_nlp2cmd
        ├── README
            ├── run
            ├── run
            ├── run
            ├── run
            ├── run
            ├── run
        ├── README
            ├── guide
            ├── demo_versioned_schemas
            ├── README
        ├── README
            ├── demo_auto
            ├── demo_batch
            ├── README_WEB_BACKEND
            ├── prompt
            ├── demo
            ├── web_app_example
            ├── nlp2cmd_web_controller
            ├── README
                ├── chat-service-docker-compose
                ├── chat-service-config
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
            ├── comparison_demo
            ├── practical_usage
            ├── simple_demo
            ├── README
            ├── usage_example
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
            ├── infrastructure_health
            ├── log_analysis
            ├── config_validation
        ├── README
            ├── benchmark_report
            ├── benchmark
            ├── README
            ├── sequential_benchmark_results
            ├── benchmark
        ├── README
            ├── workflows
            ├── advanced
            ├── llm_integration
            ├── example
            ├── README
            ├── example
                        ├── kubectl_dynamic_schema
            ├── generated_appspec
            ├── example
            ├── README
            ├── environment_analysis
            ├── schema_cache
            ├── runtime_schemas
            ├── appspec_cache
            ├── feedback_loop
            ├── 01_basics_shell_nlp2cmd
            ├── generated_shell_dynamic_schema
            ├── example
            ├── README
            ├── generated_shell_appspec
            ├── 01_basics_docker_nlp2cmd
            ├── file_repair
            ├── example
                        ├── appspec
        ├── run
        ├── _run_utils
        ├── ANALYSIS
        ├── CHANGELOG
        ├── README
            ├── run
            ├── README
                ├── 03_adaptive_20260303_143144
                ├── 03_adaptive_20260303_170926
                ├── 03_adaptive_20260303_145342
                ├── 03_adaptive_20260303_171825
                ├── 03_adaptive_20260303_145059
                ├── 03_adaptive_20260303_170902
            ├── run
            ├── README
            ├── run
            ├── README
                ├── 02_picsart_20260303_144722
                ├── 02_picsart_20260303_144922
                ├── 02_picsart_20260303_171011
                ├── 02_picsart_20260303_142942
            ├── run
            ├── README
            ├── run
            ├── README
            ├── run
            ├── README
            ├── run
            ├── README
            ├── 01_draw_chat_shapes_nlp2cmd
            ├── 02_picsart_painting
            ├── 01_draw_chat_shapes
            ├── 05_autonomous_drawing
            ├── 02_picsart_painting_nlp2cmd
            ├── 03_adaptive_drawing_nlp2cmd
            ├── 04_object_database_drawing
            ├── 03_adaptive_drawing
            ├── run
            ├── README
                ├── 01_draw_chat_20260303_170506
                ├── 01_draw_chat_20260303_170742
                ├── 01_draw_chat_20260303_143953
                ├── 01_draw_chat_20260303_144543
                ├── 01_draw_chat_20260303_171110
                ├── 01_draw_chat_20260303_170840
                ├── 01_draw_chat_20260303_171804
                ├── 01_draw_chat_20260303_144325
                ├── 01_draw_chat_20260303_142823
                ├── 01_draw_chat_20260303_170729
                ├── 01_draw_chat_20260303_142425
                ├── 01_draw_chat_20260303_142636
            ├── run
            ├── README
                ├── validation_star_red
        ├── example_ssh
        ├── example_libvirt
        ├── example_rtsp
        ├── example_multi_stream
        ├── example_http_api
        ├── README
        ├── 04_oferteo_extraction
        ├── 01_screenshot_only
        ├── 03_interactive_mode
        ├── 02_video_only
        ├── 07_batch_multiple
        ├── 05_simple_formfill
        ├── 06_formfill_with_discovery
        ├── README
        ├── terminal_session
        ├── calculator_session
        ├── multi_app_session
        ├── README
            ├── run
            ├── README
            ├── run
            ├── README
            ├── run
            ├── README
            ├── run
            ├── README
            ├── run
            ├── README
            ├── run
            ├── README
            ├── run
            ├── README
                ├── session
            ├── run
            ├── README
            ├── run
            ├── README
            ├── run
            ├── README
        ├── 03_adaptive_code_nlp2cmd
        ├── 01_codepen_live_nlp2cmd
        ├── 02_mycompiler_run
        ├── 04_jsfiddle_frontend
        ├── 03_adaptive_code
        ├── 02_mycompiler_run_nlp2cmd
        ├── 04_jsfiddle_frontend_nlp2cmd
        ├── 01_codepen_live
        ├── 05_dynamic_executor_nlp2cmd
        ├── 05_dynamic_executor
        ├── README
        ├── benchmark_before
        ├── test_feedback_results
        ├── benchmark_validator
        ├── benchmark_after
        ├── test_results
        ├── demo_validation
        ├── README
        ├── SUMMARY
        ├── api_key_prompts
    ├── 04_domain_specific/
        ├── _demo_helpers
        ├── run_all
        ├── README
            ├── mock_test_polish_llm
            ├── download_bielik
            ├── setup_and_test_bielik
            ├── README
            ├── example_pdf_search
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
            ├── example
            ├── example
            ├── example
            ├── dsl_demo
            ├── example
            ├── example
            ├── example
            ├── example
            ├── example
            ├── example
            ├── example
            ├── complete_examples
            ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
            ├── commands_demo
            ├── keywords
            ├── generator
            ├── validation_report
            ├── validation
            ├── intents
            ├── simple_demo
            ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
                ├── run
                ├── demo
                ├── README
            ├── example
    ├── llm_benchmark
    ├── thermodynamic_benchmark
    ├── learning_benchmark
    ├── README
    ├── web_schema_test_results
    ├── ci_test_results
    ├── multi_site_test_results
    ├── enhanced_context_test_results
    ├── benchmark_report
    ├── comprehensive_test_results
    ├── sequential_benchmark_results
    ├── generated_commands
    ├── nlp2cmd_monitoring_log
        ├── test_results_with_llm
        ├── test_results_no_llm
        ├── intelligent_nlp2cmd_results
    ├── chciałbym aby moja aplikacja realziowała złożone r
    ├── skąd wziąć dane weektorowej postaci obeiktow jak z
    ├── skad pobrac np 1000 takich obiektow, albo jeden pl
    ├── co można zrobić z tego typu hardkodowanymi zmienny
        ├── pipeline_runner
        ├── pipeline_runner_utils
        ├── schema_driven
        ├── polish_support
        ├── pipeline_runner_desktop
    ├── nlp2cmd/
        ├── optimization_report
        ├── __main__
        ├── appspec_runtime
        ├── pipeline_runner_shell
        ├── pipeline_runner_browser
        ├── evolutionary_orchestrator
        ├── pipeline_runner_plans
        ├── ir
            ├── resources
            ├── token_costs
        ├── monitoring/
        ├── schemas/
            ├── base
            ├── token_extractor
            ├── form_extractor
            ├── page_schema_extractor
        ├── page_schema/
            ├── radio_extractor
            ├── copy_button_extractor
            ├── button_extractor
            ├── action_planner
            ├── drawing_blueprints
            ├── schema_fallback
            ├── complex_planner
            ├── password_store
            ├── feedback_loop
            ├── step_validator
        ├── automation/
            ├── vector_store
            ├── service_configs
            ├── mouse_controller
            ├── shape_planner
            ├── captcha_solver
            ├── firefox_sessions
            ├── env_extractor
            ├── semantic_matcher_optimized
            ├── evolutionary_cache
            ├── train_model
            ├── regex
            ├── fuzzy_schema_matcher
            ├── auto_repair
            ├── thermodynamic
            ├── ml_intent_classifier
            ├── multi_command
            ├── pipeline_components
            ├── complex_detector
            ├── enhanced_context
        ├── generation/
            ├── semantic_entities
            ├── thermodynamic_components
            ├── data_loader
            ├── template_generator
            ├── pipeline
            ├── llm_multi
            ├── validating
            ├── hybrid
            ├── llm_simple
            ├── structured
                ├── generator
                ├── adapter
            ├── schema/
                ├── kubernetes_templates
                ├── rag_templates
                ├── iot_templates
                ├── shell_templates
            ├── templates/
                ├── package_mgmt_templates
                ├── git_templates
                ├── sql_templates
                ├── ffmpeg_templates
                ├── docker_templates
                ├── desktop_templates
                ├── browser_templates
                ├── data_templates
                ├── media_templates
                ├── api_templates
                ├── devops_templates
                ├── remote_templates
                ├── presentation_templates
                ├── keyword_patterns
                ├── keyword_detector
            ├── keywords/
        ├── validators/
            ├── base
            ├── backend_detector
            ├── window_manager
        ├── desktop_executor/
            ├── env_manager
            ├── browser_controller
            ├── keyboard_controller
            ├── desktop_action_executor
            ├── cli
        ├── service/
            ├── docker_app
            ├── base
            ├── vector_planner
            ├── llm_planner
            ├── blueprint_planner
        ├── canvas_planner/
            ├── rule_planner
            ├── orchestrator
            ├── base
            ├── browser_connector
            ├── existing_browser_manager
            ├── token_navigator
        ├── browser_manager/
            ├── cdp_detector
            ├── browser_setup
            ├── step_orchestrator
        ├── plan_execution/
            ├── plan_executor
        ├── planner/
            ├── core_models
        ├── core/
            ├── core_transform
            ├── core_backends
            ├── toon_integration
            ├── config
            ├── normalizer
        ├── nlp/
            ├── intent_matcher
            ├── entity_resolver
        ├── storage/
            ├── per_command_store
            ├── versioned_store
            ├── base
            ├── token_navigator
        ├── browser_token/
            ├── browser_launcher
            ├── hf_token_retriever
            ├── token_prompt_handler
            ├── web_schema
            ├── display
            ├── helpers
            ├── auto_repair
        ├── cli/
            ├── session_logger
            ├── syntax_cache
            ├── markdown_output
            ├── history
            ├── main
            ├── debug_info
            ├── cache
                ├── examples
                ├── tools
                ├── doctor
                ├── interactive
                ├── generate
            ├── commands/
                ├── run
            ├── site_explorer
            ├── form_data_loader
        ├── web_schema/
            ├── extractor
            ├── history
            ├── browser_config
            ├── form_handler
            ├── media_recorder
            ├── base
            ├── runner
            ├── browser
        ├── execution/
            ├── executor_registry
            ├── shell_executor
            ├── base
        ├── exploration/
            ├── disk
            ├── data_tree
            ├── resource_discovery
            ├── service
        ├── aggregator/
        ├── nlp_enhanced/
            ├── engine
            ├── store
            ├── runner
        ├── evolutionary/
            ├── planner
            ├── types
            ├── vision
            ├── validator
            ├── openrouter
        ├── llm/
            ├── router
            ├── repair
            ├── adaptive_learner
            ├── semantic_shell
        ├── nlp_light/
        ├── skills/
                ├── engine
                ├── skill
            ├── search/
                ├── nl_parser
                ├── object_fetcher
                ├── skill
                ├── correction_engine
                ├── commands
                ├── events
                ├── colors
            ├── drawing/
                ├── navigation
                ├── shapes
                ├── text_to_shape
                ├── validation
                ├── queries
                ├── draw_object
                ├── visual_validator
                ├── event_store
                    ├── base
                ├── renderers/
                    ├── playwright
                    ├── svg
        ├── registry/
            ├── energy_models
        ├── thermodynamic/
        ├── executor/
            ├── engine
        ├── orchestration/
            ├── metrics
            ├── handlers
            ├── reflection
            ├── dynamic
            ├── dql
            ├── base
            ├── docker
            ├── browser
        ├── adapters/
            ├── kubernetes
            ├── shell_generators
            ├── sql
            ├── shell
            ├── desktop
            ├── appspec
            ├── canvas
            ├── playwright_installer
            ├── external_cache
        ├── utils/
            ├── yaml_compat
            ├── data_files
        ├── environment/
        ├── context/
            ├── disambiguator
            ├── base
            ├── rdp_stream
            ├── ws_stream
        ├── streams/
            ├── router
            ├── vnc_stream
            ├── ssh_stream
            ├── http_stream
            ├── rtsp_stream
            ├── libvirt_stream
            ├── spice_stream
            ├── ftp_stream
        ├── enhanced/
            ├── toon_parser
        ├── feedback/
        ├── router/
            ├── link_extractor
            ├── base
            ├── field_classifier
        ├── page_analysis/
            ├── iframe_analyzer
            ├── form_analyzer
            ├── page_analyzer
            ├── command_detector
            ├── phrase_database
            ├── multilingual_phrases
            ├── form_data
            ├── shell_execution_policy
            ├── defaults
            ├── patterns
            ├── templates
            ├── router_config
            ├── optimization_schema
            ├── form_schema
            ├── semantic_embeddings
            ├── keyword_intent_detector_config
            ├── expanded_phrases
                ├── selectors
                ├── junk_field_patterns
                ├── contact_paths
                ├── services
                ├── intents
            ├── generator
            ├── adapter
        ├── schema_based/
        ├── history/
            ├── tracker
            ├── python_extractors
            ├── extractors
            ├── registry
            ├── script_extractors
        ├── schema_extraction/
            ├── llm_extractor
            ├── base
            ├── save
            ├── registry
            ├── companies
        ├── dom_actions/
            ├── navigation
            ├── forms
            ├── dispatcher
            ├── interaction
            ├── base
            ├── registry
            ├── drawing
        ├── step_handlers/
            ├── session
            ├── extraction
            ├── navigate
            ├── dispatcher
            ├── dynamic_generator
            ├── command_detector
            ├── version_aware_generator
        ├── cli
        ├── extract
    ├── app2schema/
        ├── __main__
        ├── start-vnc
        ├── docker-compose
        ├── Dockerfile
            ├── demo_desktop_gui
        ├── comprehensive_command_scanner
        ├── non_llm_schema_extractor
        ├── update_schemas
        ├── enhanced_schema_generator
        ├── intelligent_schema_generator
        ├── cmd2schema
        ├── validate_schemas
        ├── intelligent_command_generator
        ├── generate_cmd_from_prompts
        ├── generate_cmd_simple
        ├── analyze_version_detection
        ├── compare_llm
        ├── compare_batches
        ├── quick_test_nlp2cmd
    ├── setup_external
    ├── bump_version
    ├── test_commands_docker
    ├── install_desktop_tools
        ├── termo1
        ├── termo
        ├── termo_demo
        ├── termo2
        ├── implement_core_integration
        ├── implement_high_priority_fixes
        ├── final_analysis_and_next_steps
        ├── refactor_detect_normalized
        ├── refactoring_summary
        ├── restore_system
        ├── apply_polish_integration
        ├── auto_apply_refactors
        ├── cyclomatic_complexity_refactor_report
        ├── apply_nlp2cmd_fixes
        ├── split_pipeline_runner
        ├── apply_refactors_to_source
        ├── llx_refactor
        ├── generate_refactor_report
        ├── refactor_shell_entities
        ├── final_project_summary
        ├── fix_comprehensive_test_issues
        ├── apply_complexity_refactors
        ├── run_e2e_tests
        ├── compare_entity_extractors
    ├── litellm_config
    ├── README
    ├── refactoring_plan
    ├── benchmark_command_errors
    ├── benchmark_results
    ├── learning_benchmark
    ├── phrase_database
    ├── enhanced_domain_patterns
    ├── patterns
    ├── enhanced_intents
    ├── templates
    ├── prompt
    ├── form_schema
    ├── domain_weights
    ├── polish_shell_patterns
    ├── polish_table_mappings
    ├── polish_intent_mappings
        ├── minimize_all
        ├── new_tab
        ├── navigate
        ├── email_check
        ├── close_app
        ├── screenshot
        ├── open_app
        ├── draw
        ├── email_compose
        ├── shapes
        ├── colors
        ├── apps
    ├── analiza_workflow
    ├── capture_script
    ├── compare_screenshots
    ├── test_openrouter_workflow
    ├── analyze_screenshots
    ├── raport_testu
```

## API Overview

### Classes

- **`DynamicOrchestrator`** — Backward-compatible wrapper around nlp2cmd.orchestration.Orchestrator.
- **`OutputFormat`** — Format wyjściowy.
- **`ExecutionResult`** — Wynik wykonania.
- **`ResultAggregator`** — Agregator wyników.
- **`RoutingDecision`** — Decyzja routingu.
- **`DecisionRouter`** — Prosty router decyzji.
- **`ExecutionResult`** — Wynik wykonania kroku.
- **`PlanExecutor`** — Wykonawca planu.
- **`PlanStep`** — Pojedynczy krok planu.
- **`LLMPlanner`** — Mock LLM Planner.
- **`IntelligentNLP2CMD`** — NLP2CMD with automatic version detection and adaptation.
- **`CommandRequest`** — —
- **`CommandResponse`** — —
- **`HistoryResponse`** — —
- **`ServiceType`** — Types of services that can be managed.
- **`ServiceConfig`** — Configuration for a managed service.
- **`DeploymentPlan`** — Plan for deploying services.
- **`OutputFileManager`** — Manages saving generated configurations to files.
- **`DockerManager`** — Manages Docker Compose operations and container lifecycle.
- **`NLCommandParser`** — Parse natural language commands into structured actions.
- **`NLP2CMDWebController`** — Main controller for NLP2CMD-powered web infrastructure.
- **`NLP2CMDWebAPI`** — Example web API integration for NLP2CMD.
- **`Service`** — Konfiguracja pojedynczej usługi.
- **`DeployCommand`** — Komenda wdrożenia.
- **`InfraCommand`** — Komenda zarządzania infrastrukturą.
- **`SimpleServiceConfig`** — Uproszczona konfiguracja usługi.
- **`DeploymentPlan`** — Plan wdrożenia wielu usług.
- **`ServiceType`** — Typy usług obsługiwanych przez nlp2cmd.
- **`ServiceConfig`** — Konfiguracja usługi do wdrożenia.
- **`OldSystemLoader`** — Mock old system using separate JSON/YAML files
- **`SimpleToonParser`** — Simplified TOON parser for demo
- **`ToonDemo`** — Demo class showing TOON usage patterns
- **`OldSystemLoader`** — Mock starego systemu używający osobnych plików JSON/YAML.
- **`MockLLMBackend`** — Mock LLM backend for demonstration.
- **`ExampleLogger`** — Structured logger that writes to both file and console.
- **`ExampleRunner`** — Context manager for running drawing examples with full instrumentation.
- **`Shape2D`** — Represents a 2D shape with mathematical definition.
- **`ShapeDatabase`** — Autonomous shape database with online fetching and caching.
- **`SceneComposer`** — Composes multiple objects into a scene with automatic layout.
- **`BenchmarkCase`** — A single benchmark test case.
- **`CaseResult`** — —
- **`PromptExample`** — Single prompt example with expected behavior.
- **`MockPolishLLMClient`** — Mock Polish LLM client for testing without actual model.
- **`MockPolishNLP2CMD`** — Mock Polish NLP2CMD integration.
- **`BielikSetup`** — Automatyczna konfiguracja modelu Bielik.
- **`PolishPDFSearchLLM`** — Integracja polskiego LLM do wyszukiwania plików PDF.
- **`MockPolishPDFSearchLLM`** — Mock implementation dla demonstracji bez prawdziwego LLM.
- **`PDFExtractor`** — Ekstraktor tekstu z PDF.
- **`PDFExtractor`** — —
- **`TextChunker`** — —
- **`LLMSearcher`** — —
- **`PDFSearchPipeline`** — Pełny pipeline wyszukiwania w PDF.
- **`SearchResult`** — Wynik wyszukiwania.
- **`ResultsRanker`** — Ranks and filters search results.
- **`TextChunker`** — Dzieli tekst na fragmenty odpowiednie dla LLM.
- **`LLMSearcher`** — Wyszukiwanie informacji za pomocą LLM.
- **`BlastCommand`** — Komenda BLAST.
- **`SequenceCommand`** — Komenda do analizy sekwencji.
- **`ConversionCommand`** — Komenda konwersji formatów.
- **`PipelineStep`** — Krok w pipeline.
- **`FileCommand`** — Komenda przetwarzania plików.
- **`CommandTest`** — Test case dla komendy shell.
- **`ShellCommandValidator`** — Walidator komend shell.
- **`FileOperationTest`** — Test operacji na plikach.
- **`ValidationResult`** — Wynik walidacji.
- **`AdvancedValidator`** — Zaawansowany walidator komend.
- **`NetworkCommandTest`** — Test komendy sieciowej.
- **`SystemCommandTest`** — Test komendy systemowej.
- **`CommandTest`** — Test case dla komendy shell.
- **`SimpleTestRunner`** — Prosty runner testów.
- **`QueryResult`** — —
- **`BenchmarkResults`** — —
- **`BenchmarkResult`** — Result of a benchmark run.
- **`PipelineRunner`** — PipelineRunner composed from execution mixins.
- **`ShellExecutionPolicy`** — —
- **`RunnerResult`** — —
- **`VideoRecorder`** — Video recording manager for Playwright browser automation.
- **`MatchResult`** — —
- **`SchemaDrivenNLP2CMD`** — —
- **`PolishLanguageSupport`** — Polish language support for NLP2CMD
- **`DesktopExecutionMixin`** — Desktop automation and static utility methods for PipelineRunner.
- **`AppAction`** — —
- **`AppSpec`** — —
- **`ShellExecutionMixin`** — Shell command execution methods for PipelineRunner.
- **`BrowserExecutionMixin`** — DOM/browser execution methods for PipelineRunner.
- **`PlanExecutionMixin`** — Multi-step ActionPlan execution methods for PipelineRunner.
- **`ActionIR`** — —
- **`ResourceMetrics`** — Resource consumption metrics.
- **`ResourceMonitor`** — Monitor system resource usage during command execution.
- **`TokenCostEstimate`** — Token cost estimation based on resource consumption.
- **`TokenCostEstimator`** — Converts resource metrics to token equivalents.
- **`FileFormatSchema`** — Definition of a file format schema.
- **`SchemaRegistry`** — Registry for file format schemas with validation and repair capabilities.
- **`PageSchema`** — Schema of actionable elements extracted from a page.
- **`ExtractorBase`** — Base protocol for element extractors.
- **`TokenExtractor`** — Extract elements that look like API tokens/keys.
- **`FormExtractor`** — Extract visible text input fields and textareas.
- **`PageSchemaExtractor`** — Extract complete page schema using multiple specialized extractors.
- **`RadioExtractor`** — Extract radio button groups (for token type selection, etc.).
- **`CopyButtonExtractor`** — Extract buttons likely used to copy tokens to clipboard.
- **`ButtonExtractor`** — Extract visible clickable elements (buttons, role=button, etc.).
- **`ActionStep`** — Single step in an execution plan.
- **`ActionPlan`** — Complete execution plan for a complex command.
- **`ActionPlanner`** — Decomposes complex NL commands into ActionPlan via rules or LLM.
- **`DrawStep`** — Single drawing step in a blueprint.
- **`FallbackContext`** — Context collected when a step fails, used to generate alternatives.
- **`FallbackResult`** — Result of a fallback attempt.
- **`SchemaFallback`** — Generate alternative action schemas when steps fail.
- **`ActionStep`** — Single step in a complex command execution plan.
- **`ExecutionPlan`** — Complete execution plan for a complex command.
- **`ComplexCommandPlanner`** — Decomposes complex NL commands into executable action plans.
- **`Credential`** — Single credential entry.
- **`FirefoxPasswordReader`** — Read saved passwords from Firefox profile using NSS library.
- **`KeePassXCReader`** — Read passwords from KeePassXC database via CLI.
- **`BitwardenReader`** — Read passwords from Bitwarden via CLI.
- **`EnvPasswordReader`** — Read credentials from environment variables and .env files.
- **`SessionPasswordStore`** — Multi-backend password store with in-memory session cache.
- **`FailureType`** — Classification of step failure root cause.
- **`StepDiagnosis`** — Result of analyzing a step failure.
- **`RepairAttempt`** — Record of a single repair attempt.
- **`FeedbackResult`** — Result of the feedback loop for a single step.
- **`PageAnalyzer`** — Analyzes page DOM to find correct sections, selectors, and navigation targets.
- **`FeedbackLoop`** — Declarative feedback loop for browser automation steps.
- **`StepMetrics`** — Metrics collected during step execution.
- **`ValidationResult`** — Result of a pre/post condition check.
- **`StepValidator`** — Validates pre/post conditions for ActionPlan steps.
- **`DrawingPattern`** — A drawing pattern with metadata and steps.
- **`DrawingVectorStore`** — Vector database for storing and retrieving drawing patterns.
- **`Point`** — 2D point for mouse operations.
- **`MouseController`** — Advanced mouse control via Playwright with human-like movements.
- **`ShapePlanner`** — Manages a knowledge base of shapes and generates new ones via LLM.
- **`CaptchaInfo`** — Detected CAPTCHA information.
- **`CaptchaSolver`** — CAPTCHA detection and solving via LLM vision (OpenRouter → Gemini 2.5 Pro).
- **`FirefoxSessionImporter`** — Import Firefox sessions into Playwright browser profiles.
- **`ServiceConfig`** — Configuration for a known API service.
- **`EnvExtractor`** — Extracts API keys from browser sessions and saves to .env files.
- **`SemanticMatch`** — Result of semantic matching.
- **`IntentEmbedding`** — Stored embedding for an intent phrase.
- **`OptimizedSemanticMatcher`** — Optimized semantic similarity matcher using sentence embeddings.
- **`CacheEntry`** — —
- **`LookupResult`** — —
- **`EvolutionaryCache`** — Manages the .nlp2cmd/ learned schema cache.
- **`ExtractedEntity`** — A single extracted entity.
- **`ExtractionResult`** — Result of entity extraction.
- **`RegexEntityExtractor`** — Extract entities from text using regex patterns.
- **`MatchResult`** — Result of fuzzy schema matching.
- **`PhraseSchema`** — Schema for a phrase with metadata.
- **`FuzzySchemaMatcherConfig`** — Configuration for fuzzy matching thresholds.
- **`FuzzySchemaMatcher`** — Language-agnostic fuzzy matcher using JSON schemas.
- **`CommandRepairer`** — Repairs invalid commands using LLM fallback.
- **`ThermodynamicGenerator`** — Generate solutions for optimization problems using Langevin sampling.
- **`HybridThermodynamicGenerator`** — Hybrid generator combining rule/LLM-based DSL with thermodynamic optimization.
- **`SchedulingEnergy`** — Scheduling energy model for thermodynamic optimization.
- **`AllocationEnergy`** — Allocation energy model for thermodynamic optimization.
- **`RoutingEnergy`** — Routing energy model for thermodynamic optimization.
- **`IntentPrediction`** — Result of intent classification.
- **`TrainingSample`** — Single training sample.
- **`MLIntentClassifier`** — Fast ML-based intent classifier using TF-IDF + SVM.
- **`MultiCommandResult`** — Result of multi-command detection.
- **`MultiCommandDetector`** — Utility class to detect multiple commands in one input.
- **`SimpleExecutionPlan`** — Simple execution plan for adapters.
- **`PipelineResult`** — Result of the complete pipeline.
- **`PipelineMetrics`** — Track pipeline metrics for evaluation.
- **`ComplexityAnalysis`** — Result of multi-step complexity analysis.
- **`ComplexQueryDetector`** — Detects multi-step commands BEFORE the keyword detection pipeline.
- **`ContextualMatch`** — Enhanced match with semantic similarity.
- **`EnhancedContextDetector`** — Enhanced context detection using multiple NLP approaches.
- **`SemanticEntityExtractor`** — —
- **`OptimizationProblem`** — Structured optimization problem definition.
- **`ThermodynamicResult`** — Result of thermodynamic optimization.
- **`ThermodynamicProblemDetector`** — Detects optimization problems in natural language.
- **`ThermodynamicConfig`** — Configuration for thermodynamic optimization.
- **`PhraseEntry`** — Single phrase entry for intent matching.
- **`PhraseDatabase`** — Collection of phrase entries with metadata.
- **`DataLoader`** — Optimized data loader with format detection and caching.
- **`TemplateResult`** — Result of template generation.
- **`TemplateGenerator`** — Generate DSL commands from templates.
- **`RuleBasedPipeline`** — Complete rule-based NL → DSL pipeline.
- **`RoutingResult`** — Result of domain routing.
- **`LLMDomainRouter`** — Route queries to correct domain using LLM classification.
- **`MultiDomainResult`** — Result of multi-domain generation.
- **`MultiDomainGenerator`** — Generate DSL for any domain using LLM routing.
- **`CachedMultiDomainGenerator`** — Multi-domain generator with response caching.
- **`DSLValidator`** — Protocol for DSL validators.
- **`ValidationResult`** — Result of DSL validation.
- **`ValidatingGeneratorResult`** — Result of validated generation.
- **`ValidatingGenerator`** — Generate DSL with validation and self-correction.
- **`SimpleSQLValidator`** — Simple SQL syntax validator.
- **`SimpleShellValidator`** — Simple shell command validator.
- **`SimpleDockerValidator`** — Simple Docker command validator.
- **`SimpleKubernetesValidator`** — Simple Kubernetes command validator.
- **`HybridResult`** — Result of hybrid generation.
- **`HybridStats`** — Statistics for hybrid generator.
- **`HybridGenerator`** — Use rules first, LLM as fallback.
- **`AdaptiveHybridGenerator`** — Hybrid generator with adaptive threshold.
- **`LLMClient`** — Protocol for LLM client implementations.
- **`LiteLLMClient`** — —
- **`LLMConfig`** — Configuration for LLM generators.
- **`LLMGenerationResult`** — Result of LLM generation.
- **`BaseLLMGenerator`** — Base class for LLM-based DSL generators.
- **`SimpleLLMSQLGenerator`** — LLM-based SQL generation - single domain first.
- **`SimpleLLMShellGenerator`** — LLM-based Shell command generation.
- **`SimpleLLMDockerGenerator`** — LLM-based Docker command generation.
- **`SimpleLLMKubernetesGenerator`** — LLM-based Kubernetes command generation.
- **`MockLLMClient`** — Mock LLM client for testing.
- **`StructuredPlan`** — Structured execution plan from LLM.
- **`StructuredPlanResult`** — Result of structured planning.
- **`StructuredLLMPlanner`** — LLM with enforced JSON output schema.
- **`MultiStepPlan`** — Multi-step execution plan.
- **`MultiStepPlanner`** — Iteration 8: Multi-Step Plans.
- **`SchemaBasedGenerator`** — Generates commands using schemas instead of templates.
- **`SchemaRegistry`** — Registry for managing and improving schemas.
- **`SchemaDrivenAppSpecAdapter`** — AppSpec adapter that uses schema-based generation.
- **`KeywordPatterns`** — Manages keyword patterns for intent detection.
- **`DetectionResult`** — Result of intent detection.
- **`KeywordIntentDetector`** — Rule-based intent detection using keyword matching.
- **`ValidationResult`** — Result of a validation operation.
- **`BaseValidator`** — Abstract base class for validators.
- **`SyntaxValidator`** — Generic syntax validator for balanced brackets, quotes, etc.
- **`SQLValidator`** — SQL-specific validator.
- **`ShellValidator`** — Shell command validator.
- **`DockerValidator`** — Docker command and Dockerfile validator.
- **`KubernetesValidator`** — Kubernetes command and manifest validator.
- **`CompositeValidator`** — Combines multiple validators.
- **`DesktopBackend`** — Available desktop automation backends.
- **`ActionStatus`** — Status of action execution.
- **`ActionResult`** — Result of action execution.
- **`ExecutionConfig`** — Configuration for desktop execution.
- **`BackendDetector`** — Detect available desktop automation backends.
- **`WindowManager`** — Manage application windows via desktop automation tools.
- **`EnvManager`** — Manage environment variables and .env files.
- **`BrowserController`** — Control Firefox browser via command-line interface.
- **`KeyboardController`** — Send keyboard input via desktop automation tools.
- **`DesktopActionExecutor`** — Main orchestrator for executing desktop automation actions.
- **`ServiceConfig`** — Configuration for NLP2CMD service.
- **`QueryRequest`** — Request model for query endpoint.
- **`QueryResponse`** — Response model for query endpoint.
- **`NLP2CMDService`** — NLP2CMD HTTP API Service.
- **`CanvasPlanResult`** — Result of canvas planning.
- **`CanvasPlannerBase`** — Base class for canvas planners.
- **`VectorDBPlanner`** — Searches vector database for semantically similar drawing patterns.
- **`LLMCanvasPlanner`** — Generates drawing plans using LLM for arbitrary objects.
- **`BlueprintPlanner`** — Uses rich drawing blueprints (SVG paths, polygons, beziers).
- **`RuleBasedCanvasPlanner`** — Generates drawing plans using hardcoded shape rules.
- **`CanvasPlanningOrchestrator`** — Orchestrates multiple canvas planners in priority order.
- **`ConnectionStatus`** — Status of browser connection attempt.
- **`BrowserConfig`** — Configuration for browser connection.
- **`BrowserConnectionResult`** — Result of browser connection attempt.
- **`BrowserConnector`** — Connect to browsers via Playwright CDP protocol.
- **`ExistingBrowserManager`** — Orchestrator for connecting to existing browser via CDP.
- **`NavigationStatus`** — Status of navigation attempt.
- **`TokenNavigator`** — Navigate to HuggingFace token settings page.
- **`CdpDetector`** — Detect and verify CDP ports for browser connections.
- **`BrowserContextOptions`** — Options for browser context creation.
- **`BrowserSetup`** — Handles browser setup, session management, and context creation.
- **`StepResult`** — Result of executing a single step.
- **`StepOrchestrator`** — Orchestrates step execution with validation, fallback, and retry.
- **`PlanExecutor`** — Main executor for ActionPlans with browser automation.
- **`PlannerConfig`** — Configuration for LLM Planner.
- **`PlanningResult`** — Result of plan generation.
- **`LLMPlanner`** — Generates execution plans using LLM.
- **`TransformStatus`** — Status of a transformation operation.
- **`Intent`** — Represents a detected intent from natural language input.
- **`Entity`** — Represents an extracted entity from natural language input.
- **`ExecutionPlan`** — Structured plan for command execution.
- **`TransformResult`** — Result of a natural language to command transformation.
- **`NLP2CMD`** — Main class for Natural Language to Command transformation.
- **`NLPBackend`** — Base class for NLP processing backends.
- **`SpaCyBackend`** — spaCy-based NLP backend.
- **`LLMBackend`** — LLM-based NLP backend (Claude, GPT, etc.).
- **`RuleBasedBackend`** — Simple rule-based NLP backend for basic pattern matching.
- **`ToonDataManager`** — Unified data manager using TOON format
- **`ServiceConfig`** — Configuration for a known API service (mirrors env_extractor.ServiceConfig).
- **`ServiceRegistry`** — Loads and serves service configurations from ``services.yaml``.
- **`IntentConfig`** — Configuration for a single intent under a domain.
- **`IntentRegistry`** — Loads and serves intent configurations from ``intents.yaml``.
- **`NormalizedQuery`** — Immutable result of normalizing a raw user query.
- **`QueryNormalizer`** — Normalize a raw user query into a ``NormalizedQuery``.
- **`IntentDef`** — Intent definition loaded from YAML.
- **`IntentMatch`** — Result of intent matching.
- **`IntentMatcher`** — Multilingual intent matcher backed by YAML definitions.
- **`AppInfo`** — Application info loaded from apps.yaml.
- **`EntityResolver`** — Multilingual entity resolver backed by YAML data files.
- **`PerCommandSchemaStore`** — Stores each command schema in its own file.
- **`VersionedSchemaStore`** — Extended schema store that supports versioning.
- **`BrowserTokenResult`** — Result of browser token retrieval attempt.
- **`TokenConfig`** — Configuration for token retrieval.
- **`NavigationStatus`** — Status of navigation attempt.
- **`TokenNavigator`** — Navigate to token pages with URL verification.
- **`BrowserLauncher`** — Launch browser with automatic fallback from Firefox to Chromium.
- **`HFTokenRetriever`** — Main orchestrator for retrieving HuggingFace tokens via browser.
- **`TokenPromptHandler`** — Handle interactive prompts for token input.
- **`ErrorCategory`** — Categories of errors that Doctor can handle.
- **`RepairResult`** — Result of auto-repair attempt.
- **`AutoRepairSystem`** — Automatic error diagnosis and repair system.
- **`SessionLogger`** — Logs automation sessions to Markdown with inline base64 screenshots.
- **`SyntaxCache`** — Cache for Rich Syntax objects to improve performance.
- **`MarkdownConsoleProxy`** — Proxy that forces all console.print output into markdown code blocks.
- **`MarkdownBlockStream`** — Context manager that streams multiple prints inside a single Markdown block.
- **`ExampleScenario`** — Definition of an example scenario.
- **`ExamplesRegistry`** — Registry of all available example scenarios.
- **`ExamplesRunner`** — Runner for example scenarios with preconfiguration.
- **`Status`** — —
- **`CheckResult`** — —
- **`NP2CMDDoctor`** — System diagnostic and auto-repair for nlp2cmd.
- **`InteractiveSession`** — Interactive REPL session with feedback loop.
- **`PageInfo`** — Information about a discovered page.
- **`ExplorationResult`** — Result of site exploration.
- **`SiteExplorer`** — Explores website to find forms, contact pages, and other content.
- **`FormDataLoader`** — Loads form field data from multiple sources:
- **`WebElement`** — Represents an interactive element on a web page.
- **`WebPageSchema`** — Schema for a web page.
- **`WebSchemaExtractor`** — Extract schema from web pages using Playwright.
- **`InteractionRecord`** — Record of a single browser interaction.
- **`InteractionHistory`** — Tracks and learns from browser interactions.
- **`BrowserConfigLoader`** — Single source of truth for browser automation config.
- **`DynamicSelectorGenerator`** — Generate selectors dynamically using LLM when static ones fail.
- **`FormField`** — Represents a form field.
- **`FormData`** — Collected form data.
- **`FormHandler`** — Handles form detection and interactive filling.
- **`MediaRecorder`** — Manages video recording and screenshots during browser sessions.
- **`ExecutorResult`** — Unified result from any executor.
- **`ExecutorContext`** — Shared context passed to executors.
- **`BaseExecutor`** — Abstract base for all executors.
- **`ExecutionResult`** — Result of command execution.
- **`RecoveryContext`** — Context for LLM-assisted error recovery.
- **`ExecutionRunner`** — Execute commands with logging, error handling, and LLM-assisted recovery.
- **`BrowserResult`** — Result of a browser automation action.
- **`BrowserExecutor`** — Execute browser automation commands.
- **`ExecutorRegistry`** — Central registry that maps action names to executor instances.
- **`ShellExecutor`** — Execute shell commands with safety checks and error recovery.
- **`ExplorationResult`** — Result of exploration in any space.
- **`ExplorationContext`** — Context for exploration - what we're looking for.
- **`BaseExplorer`** — Abstract base class for all explorers.
- **`ExplorerRegistry`** — Registry of available explorers.
- **`FileInfo`** — Information about a file or directory.
- **`DiskExplorer`** — Explorer for file systems and disk content.
- **`DataNode`** — A node in a data tree.
- **`DataMatch`** — A match in data exploration.
- **`DataTreeExplorer`** — Explorer for nested data structures (JSON, dicts, etc.).
- **`MissingResource`** — Information about a missing resource.
- **`DiscoveryDecision`** — Decision about whether to attempt discovery or fail.
- **`ResourceDiscoveryManager`** — Manages automatic resource discovery during command execution.
- **`EndpointInfo`** — Information about an API endpoint.
- **`ServiceInfo`** — Information about a service.
- **`ServiceExplorer`** — Explorer for REST APIs, GraphQL, and other services.
- **`OutputFormat`** — Output format types.
- **`AggregatedResult`** — Aggregated result from plan execution.
- **`ResultAggregator`** — Aggregates and formats execution results.
- **`ShellGPTBackend`** — NLP backend that uses shell-gpt for intelligent command generation.
- **`HybridNLPBackend`** — Hybrid NLP backend that combines multiple approaches.
- **`EvolutionaryRecoveryEngine`** — Silnik ewolucyjnych napraw - uczy się z każdej sytuacji.
- **`EvolutionaryKnowledgeStore`** — Stores and persists learning data for recovery attempts.
- **`AutonomousExampleRunner`** — Autonomiczny runner z evolutionary recovery.
- **`EvolutionaryRecoveryPlanner`** — Chooses and executes recovery strategies.
- **`RecoveryStrategy`** — Strategie naprawy - rozszerzalne i ewolucyjne.
- **`RecoveryAttempt`** — Pojedyncza próba naprawy.
- **`ExecutionMetrics`** — Metryki wykonania - dla ciągłego doskonalenia.
- **`VisionResult`** — Result of a vision analysis.
- **`VisionAnalyzer`** — High-level vision analysis using LLM.
- **`ValidationVerdict`** — Result from LLM validator.
- **`LLMValidator`** — Validates command output against user intent using a local Ollama model.
- **`LLMResponse`** — Response from OpenRouter API.
- **`OpenRouterClient`** — OpenRouter API client with text and vision support.
- **`RouterResponse`** — Unified response from LLM Router.
- **`ModelHealth`** — Health status of a model deployment.
- **`LLMRouter`** — Smart LLM Router with multi-model support, fallbacks, and task specialization.
- **`RepairResult`** — Result from LLM repair.
- **`LLMRepair`** — Repairs failed commands and optionally patches data files using OpenRouter.
- **`ErrorPattern`** — Classified error pattern from LLM failures.
- **`ModelPerformance`** — Tracks performance metrics for a model on a specific task.
- **`LearnedRule`** — A routing rule learned from experience.
- **`AdaptiveLearner`** — Adaptive learning system for LLM routing.
- **`SemanticShellBackend`** — —
- **`SearchResult`** — Single search result.
- **`SearchConfig`** — Configuration for search engine.
- **`SearchEngine`** — Open source search engine aggregator.
- **`SearchContext`** — Context for search operations.
- **`SearchSkill`** — High-level search skill for nlp2cmd.
- **`NLDrawingParser`** — Parse natural language drawing instructions into DrawCommand sequences.
- **`FetchedShape`** — Shape data retrieved from an external database.
- **`SimpleIconsFetcher`** — Fetch SVG icons from Simple Icons (simpleicons.org).
- **`IconifyFetcher`** — Fetch icons from Iconify API (api.iconify.design).
- **`SVGRepoFetcher`** — Search and fetch from SVG Repo (svgrepo.com).
- **`ObjectFetcher`** — Autonomous shape fetcher with multi-database search and local caching.
- **`DrawingSkill`** — Facade for the drawing skill — single entry point for all drawing operations.
- **`CorrectionStep`** — A single step in a correction plan.
- **`CorrectionPlan`** — Plan of steps to correct a drawing.
- **`CorrectionResult`** — Result of applying corrections.
- **`CorrectionEngine`** — Iterative correction engine for drawing repair.
- **`AutonomousDrawingPipeline`** — Full autonomous drawing pipeline: draw → validate → correct → repeat.
- **`DrawCommand`** — Abstract base for all drawing commands.
- **`InitCanvas`** — Initialize a drawing canvas.
- **`DrawShape`** — Draw a shape on the canvas.
- **`SetColor`** — Change the active drawing color.
- **`SelectTool`** — Select a drawing tool.
- **`ClearCanvas`** — Clear the entire canvas.
- **`CommandHandler`** — Protocol for command handlers.
- **`CommandBus`** — Dispatches commands to handlers, validates, and emits events.
- **`EventType`** — —
- **`DrawingEvent`** — Base immutable event — all drawing events inherit from this.
- **`CanvasInitialized`** — Fired when a canvas is created or discovered.
- **`CanvasCleared`** — Fired when the canvas is cleared.
- **`ShapeDrawn`** — Fired when a shape is drawn on the canvas.
- **`ColorChanged`** — Fired when the active drawing color is changed.
- **`ToolSelected`** — Fired when a drawing tool is selected.
- **`ColorResolver`** — Resolves color names to hex codes with Polish + English support.
- **`NavigationState`** — State of the navigation process.
- **`CanvasInfo`** — Information about the discovered canvas.
- **`NavigationStep`** — A single step in the navigation process.
- **`NavigationResult`** — Full result of the navigation process.
- **`DrawNavigationSkill`** — Vision-guided navigation to drawing canvas.
- **`ShapeGenerator`** — Abstract shape generator — one responsibility: produce point groups.
- **`CircleGenerator`** — —
- **`EllipseGenerator`** — —
- **`RectangleGenerator`** — —
- **`SquareGenerator`** — —
- **`TriangleGenerator`** — —
- **`StarGenerator`** — —
- **`HeartGenerator`** — —
- **`SpiralGenerator`** — —
- **`HouseGenerator`** — —
- **`FlowerGenerator`** — —
- **`SunGenerator`** — —
- **`TreeGenerator`** — —
- **`LineGenerator`** — —
- **`DotGenerator`** — —
- **`GridGenerator`** — —
- **`WaveGenerator`** — —
- **`CarGenerator`** — —
- **`BirdGenerator`** — —
- **`ButterflyGenerator`** — —
- **`BoatGenerator`** — —
- **`MountainGenerator`** — —
- **`CatGenerator`** — —
- **`FishGenerator`** — —
- **`RocketGenerator`** — —
- **`CastleGenerator`** — —
- **`DiamondGenerator`** — —
- **`ArrowGenerator`** — —
- **`PentagonGenerator`** — —
- **`HexagonGenerator`** — —
- **`OctagonGenerator`** — —
- **`CrossGenerator`** — —
- **`CrescentGenerator`** — —
- **`CloudDetailedGenerator`** — —
- **`ShapeRegistry`** — Registry of all available shape generators.
- **`GeneratedShape`** — Result of LLM shape generation.
- **`DynamicShapeGenerator`** — ShapeGenerator created from LLM-generated or fetched point data.
- **`TextToShapeEngine`** — Generates 2D shapes from text descriptions using LLM.
- **`ObjectStatus`** — Status of a single requested object.
- **`ObjectAssessment`** — Vision assessment of a single requested object.
- **`TaskPlan`** — What the user wants drawn — the reference for validation.
- **`ValidationReport`** — Full validation report: what's done, what remains, what's wrong.
- **`DrawValidationSkill`** — Task-aware drawing validation using Qwen VL.
- **`DrawQuery`** — Abstract base for all drawing queries.
- **`GetCanvasState`** — Reconstruct current canvas state from events.
- **`GetDrawingHistory`** — Get the full drawing history as a list of event summaries.
- **`GetShapePoints`** — Get all shape point groups from drawn shapes (for rendering).
- **`GetLastNShapes`** — Get the last N drawn shapes.
- **`QueryBus`** — Dispatches queries against the event store.
- **`DrawStatus`** — Status of a single object draw operation.
- **`ObjectDrawResult`** — Result of drawing a single object.
- **`SceneDrawResult`** — Result of drawing multiple objects (a scene).
- **`DrawObjectSkill`** — Resolve and draw shapes with vision verification.
- **`ValidationVerdict`** — Result of visual validation.
- **`DrawingCorrection`** — A single correction to apply to the drawing.
- **`ValidationResult`** — Full result of visual validation.
- **`VisualValidator`** — Validates drawings using vision LLM models.
- **`EventStore`** — Append-only event store with optional persistence and subscriber support.
- **`Renderer`** — Abstract renderer interface.
- **`PlaywrightRenderer`** — Render drawings on a browser canvas via Playwright mouse control.
- **`SVGRenderer`** — Render drawings as SVG markup.
- **`ParamType`** — Parameter types for action validation.
- **`ParamSchema`** — Schema for an action parameter.
- **`ActionSchema`** — Schema definition for an action.
- **`ActionResult`** — Result of action execution.
- **`ActionHandler`** — Base class for action handlers.
- **`ActionRegistry`** — Central registry for all system actions.
- **`Task`** — Represents a task to be scheduled.
- **`Resource`** — Represents a resource with capacity.
- **`SchedulingEnergy`** — Energy model for scheduling problems.
- **`AllocationEnergy`** — Energy model for resource allocation problems.
- **`RoutingEnergy`** — Energy model for routing problems (TSP, VRP).
- **`CSPEnergy`** — Generic Constraint Satisfaction Problem energy model.
- **`LangevinConfig`** — Configuration for Langevin dynamics sampler.
- **`SamplerResult`** — Result from Langevin sampling.
- **`EnergyModel`** — Abstract base class for energy models.
- **`QuadraticEnergy`** — Simple quadratic energy for testing: V(z) = 0.5 * ||z - target||²
- **`ConstraintEnergy`** — Energy model for constraint satisfaction problems.
- **`LangevinSampler`** — Thermodynamic sampler using overdamped Langevin dynamics.
- **`EntropyProductionRegularizer`** — Regularizer based on Whitelam's principle:
- **`MajorityVoter`** — Select best sample from multiple candidates.
- **`ThermodynamicRouter`** — Routes problems to appropriate solver:
- **`EnergyEstimator`** — Estimate computational energy consumption.
- **`StepStatus`** — Status of a plan step.
- **`PlanStep`** — A single step in an execution plan.
- **`StepResult`** — Result of executing a single step.
- **`ExecutionPlan`** — Multi-step execution plan.
- **`ExecutionContext`** — Context for plan execution.
- **`ExecutionResult`** — Result of executing a complete plan.
- **`PlanValidator`** — Validates execution plans against action registry.
- **`PlanExecutor`** — Executes multi-step plans.
- **`StepStatus`** — —
- **`StepDef`** — Definition of a single orchestration step.
- **`StepResult`** — Result of executing a single step.
- **`TaskSchema`** — LLM-generated execution plan — a dynamic schema for the task.
- **`TaskResult`** — Final result of orchestrated task execution.
- **`Orchestrator`** — LLM-driven orchestration engine with reflection.
- **`StepMetric`** — Metrics for a single orchestration step.
- **`TaskMetric`** — Metrics for a complete orchestrated task.
- **`LearnedPath`** — A successful decision path that can be reused for similar goals.
- **`GeneratedFunction`** — A generated JS or Python function cached for reuse.
- **`MetricsCollector`** — Collects and persists orchestration metrics.
- **`PathOptimizer`** — Stores successful decision paths for reuse on similar goals.
- **`FunctionCache`** — Caches auto-generated JS and Python functions in .nlp2cmd/generated/.
- **`ReflectionVerdict`** — Outcome of result analysis.
- **`ReflectionResult`** — Result of LLM-driven reflection on execution output.
- **`ResultAnalyzer`** — Analyzes execution results using LLM for intelligent reflection.
- **`DynamicSafetyPolicy`** — Enhanced safety policy that adapts based on extracted schemas.
- **`DynamicAdapter`** — Dynamic adapter that uses extracted schemas instead of hardcoded patterns.
- **`DQLSafetyPolicy`** — DQL-specific safety policy.
- **`EntityContext`** — Doctrine entity context.
- **`DQLAdapter`** — DQL adapter for Doctrine ORM queries.
- **`SafetyPolicy`** — Base safety policy configuration.
- **`AdapterConfig`** — Configuration for DSL adapters.
- **`BaseDSLAdapter`** — Abstract base class for Domain-Specific Language adapters.
- **`DockerSafetyPolicy`** — Docker-specific safety policy.
- **`ComposeContext`** — Docker Compose context.
- **`DockerAdapter`** — Docker adapter for CLI and Compose operations.
- **`BrowserSafetyPolicy`** — —
- **`BrowserAdapter`** — Minimal adapter that turns NL into dom_dql.v1 navigation (Playwright).
- **`KubernetesSafetyPolicy`** — Kubernetes-specific safety policy.
- **`ClusterContext`** — Kubernetes cluster context.
- **`KubernetesAdapter`** — Kubernetes adapter for kubectl commands and manifests.
- **`FileOperationGenerator`** — Generator for file operations.
- **`ProcessManagementGenerator`** — Generator for process management commands.
- **`NetworkGenerator`** — Generator for network commands.
- **`SystemMaintenanceGenerator`** — Generator for system maintenance commands.
- **`DevelopmentGenerator`** — Generator for development commands.
- **`GitGenerator`** — Generator for git commands.
- **`DockerGenerator`** — Generator for docker commands.
- **`TextProcessingGenerator`** — Generator for text processing commands.
- **`SQLSafetyPolicy`** — SQL-specific safety policy.
- **`SchemaContext`** — Database schema context for SQL generation.
- **`SQLAdapter`** — SQL adapter supporting multiple database dialects.
- **`ShellSafetyPolicy`** — Shell-specific safety policy.
- **`EnvironmentContext`** — System environment context.
- **`ShellAdapter`** — Shell adapter supporting multiple shell types.
- **`DesktopAction`** — Structured desktop automation action.
- **`DesktopSafetyPolicy`** — Safety policy for desktop GUI automation.
- **`DesktopAdapter`** — Adapter for desktop GUI automation via VNC/noVNC + xdotool/wmctrl.
- **`AppSpecAdapterConfig`** — —
- **`AppSpecAdapter`** — —
- **`DrawingStep`** — Single step in a drawing plan.
- **`DrawingPlan`** — Complete drawing plan for canvas operations.
- **`CanvasSafetyPolicy`** — Safety policy for canvas operations — generally safe.
- **`CanvasAdapter`** — Adapter for canvas-based drawing via Playwright mouse control.
- **`ExternalCacheManager`** — Manages caching of external dependencies like Playwright browsers.
- **`ToolInfo`** — Information about an installed tool.
- **`ServiceInfo`** — Information about a running service.
- **`EnvironmentReport`** — Complete environment analysis report.
- **`EnvironmentAnalyzer`** — Analyzes the system environment for available tools, services,
- **`DisambiguationResult`** — Result of disambiguation process.
- **`CommandDisambiguator`** — Disambiguates commands using history context.
- **`StreamResult`** — Result of a stream operation.
- **`SourceURI`** — Parsed --source URI.
- **`StreamAdapter`** — Base class for all stream protocol handlers.
- **`RDPStreamAdapter`** — —
- **`WSStreamAdapter`** — —
- **`StreamRouter`** — Routes --source URIs to the correct protocol handler.
- **`VNCStreamAdapter`** — —
- **`SSHStreamAdapter`** — —
- **`HTTPStreamAdapter`** — —
- **`RTSPStreamAdapter`** — Analyze RTSP video streams — colors, motion, objects.
- **`LibvirtStreamAdapter`** — Manage VMs via libvirt and control their desktops via SPICE/VNC.
- **`SPICEStreamAdapter`** — —
- **`FTPStreamAdapter`** — —
- **`EnhancedNLP2CMD`** — Enhanced NLP2CMD with dynamic schema capabilities.
- **`ToonNodeType`** — TOON node types
- **`ToonNode`** — TOON node structure
- **`ToonParser`** — Unified TOON format parser with hierarchical access
- **`FeedbackType`** — Types of feedback from the system.
- **`FeedbackResult`** — Result of feedback analysis.
- **`CorrectionRule`** — Rule for automatic correction.
- **`FeedbackAnalyzer`** — Analyzes transformation results and provides feedback.
- **`CorrectionEngine`** — Engine for applying corrections to generated content.
- **`RoutingDecision`** — Routing decision types.
- **`RoutingResult`** — Result of routing decision.
- **`RouterConfig`** — Configuration for Decision Router.
- **`DecisionRouter`** — Routes incoming requests to appropriate processing path.
- **`LinkExtractor`** — Extract and normalize links from page.
- **`FieldInfo`** — Information about a form field.
- **`PageAnalysisResult`** — Result of page analysis.
- **`FieldClassifier`** — Classify form fields as contact-like or junk (search, cookie, etc.).
- **`IframeAnalyzer`** — Analyze iframes for embedded forms (common for contact widgets).
- **`FormAnalyzer`** — Analyze page for forms and form fields.
- **`PageAnalyzer`** — Main orchestrator for page analysis.
- **`SchemaUsage`** — Record of schema usage.
- **`CommandRecord`** — Record of a command execution.
- **`CommandHistory`** — Unified command history tracker.
- **`PythonCodeExtractor`** — Extract command schemas from Python source code with decorators.
- **`ClickExtractor`** — Specialized extractor for Click applications.
- **`CommandParameter`** — Represents a command parameter extracted from schema.
- **`CommandSchema`** — Dynamic command schema extracted from various sources.
- **`ExtractedSchema`** — Container for extracted schemas from a source.
- **`OpenAPISchemaExtractor`** — Extract command schemas from OpenAPI/Swagger specifications.
- **`ShellHelpExtractor`** — Extract command schemas from shell help output.
- **`SchemaRegistry`** — Registry for managing dynamically extracted schemas.
- **`ShellScriptExtractor`** — Extract schema from a shell script file using shlex/regex heuristics.
- **`MakefileExtractor`** — Extract schema from Makefile targets and variables.
- **`LLMSchemaExtractor`** — Extract command schemas using LLM assistance.
- **`ActionContext`** — Context passed to DOM action handlers.
- **`ActionResult`** — Result from a DOM action handler.
- **`DomAction`** — Base class for DOM action handlers.
- **`SaveToFileAction`** — Save extracted data to a text file.
- **`SaveToCsvAction`** — Save extracted data to a CSV file.
- **`ActionRegistry`** — Registry mapping action names to their handlers.
- **`ExtractCompaniesAction`** — Extract company information from catalog pages.
- **`NavigateAction`** — Navigate to a URL.
- **`ExploreForContentAction`** — Explore site to find content.
- **`ExploreForFormAction`** — Explore site to find forms.
- **`FillFormAction`** — Fill form fields automatically from .env and data files.
- **`ActionDispatcher`** — Dispatches DOM actions to appropriate handlers.
- **`ClickHandler`** — Handle click action with retry logic for detached elements.
- **`ClickRadioHandler`** — Handle click_radio action for radio button selection.
- **`DismissOverlayHandler`** — Handle dismiss_overlay action for cookie banners and dialogs.
- **`TypeTextHandler`** — Handle type_text action with fallback selectors.
- **`FillFormHandler`** — Handle fill_form action for multiple fields.
- **`SubmitFormHandler`** — Handle submit_form action.
- **`LoginHandler`** — Handle login action with email and password.
- **`NewTabHandler`** — Handle new_tab action.
- **`WaitHandler`** — Handle wait action.
- **`ScreenshotHandler`** — Handle screenshot action.
- **`HandlerContext`** — Context passed to step handlers during execution.
- **`HandlerResult`** — Result from a step handler execution.
- **`StepHandler`** — Base class for plan step handlers.
- **`HandlerRegistry`** — Registry mapping action names to their handlers.
- **`CanvasMixin`** — Mixin providing canvas selection logic.
- **`WaitForCanvasHandler`** — Wait for canvas element to appear.
- **`GetCanvasCenterHandler`** — Get canvas center coordinates.
- **`SelectToolHandler`** — Select a drawing tool.
- **`SetColorHandler`** — Set foreground color for drawing.
- **`SetLineWidthHandler`** — Set line width for drawing.
- **`DrawCircleHandler`** — Draw a circle on canvas.
- **`DrawFilledCircleHandler`** — Draw a filled circle on canvas with verification.
- **`DrawFilledEllipseHandler`** — Draw a filled ellipse on canvas.
- **`DrawFilledRectangleHandler`** — Draw a filled rectangle on canvas.
- **`DrawRectangleHandler`** — Draw a rectangle on canvas.
- **`DrawLineHandler`** — Draw a line on canvas with simple pixel verification.
- **`DrawEllipseHandler`** — Draw an ellipse outline on canvas.
- **`DrawArcHandler`** — Draw an arc on canvas.
- **`DrawPolygonHandler`** — Draw a polygon on canvas.
- **`DrawBezierHandler`** — Draw a bezier path on canvas.
- **`DrawSvgPathHandler`** — Draw an SVG path on canvas.
- **`FillAtHandler`** — Click/fill at the current canvas offset.
- **`ClickCanvasHandler`** — Click the canvas at an offset.
- **`CheckSessionHandler`** — Check if user is logged into a service with auto-login via password store.
- **`SubmitAndExtractKeyHandler`** — Submit form and poll for API key extraction.
- **`DiscoverServiceSectionHandler`** — Discover service section (e.g., API keys page) by link discovery.
- **`ExtractKeyHandler`** — Extract API key from page DOM and clipboard.
- **`ExtractApiKeyHandler`** — Disabled safety-only alias for API key extraction.
- **`CheckClipboardHandler`** — Validate clipboard content against key pattern.
- **`SaveEnvHandler`** — Save value to .env file.
- **`VerifyEnvHandler`** — Verify that env var was saved to .env file.
- **`PromptSecretHandler`** — Prompt user for secret/API key with timeout and validation.
- **`EchoHandler`** — Echo a message to the console.
- **`ExtractTextHandler`** — Extract text from page elements.
- **`NavigateHandler`** — Handle navigate action - navigate to URL with security checkup handling.
- **`StepDispatcher`** — Dispatches plan steps to appropriate handlers.
- **`DynamicSchemaGenerator`** — Generates schemas dynamically without hardcoding.
- **`CommandMatch`** — Represents a matched command with confidence.
- **`CommandDetector`** — Detects shell commands from natural language descriptions.
- **`VersionAwareCommandGenerator`** — Generates commands with automatic version detection.
- **`App2SchemaResult`** — —
- **`OptionType`** — Types of command options.
- **`ParsedOption`** — Parsed command option.
- **`ComprehensiveCommandScanner`** — Scanner that extracts ALL command options.
- **`NonLLMStrategy`** — Available non-LLM strategies.
- **`SchemaQuality`** — Schema quality metrics.
- **`NonLLMSchemaExtractor`** — Non-LLM schema extractor with multiple strategies.
- **`ExtractionStrategy`** — Available extraction strategies.
- **`ExtractionResult`** — Result of schema extraction.
- **`EnhancedSchemaExtractor`** — Enhanced schema extractor with multiple strategies.
- **`CommandInfo`** — Information about a command.
- **`IntelligentSchemaExtractor`** — Extracts schemas using intelligent analysis instead of hardcoded keywords.
- **`CommandSchemaGenerator`** — Generate schemas for command-line tools.
- **`GenerationMethod`** — Available generation methods.
- **`GenerationResult`** — Result of command generation.
- **`IntelligentCommandGenerator`** — Intelligent command generator with adaptive strategies.
- **`CommandGenerator`** — Generate commands from prompts using NLP2CMD.
- **`HyperparameterSpace`** — Przestrzeń hiperparametrów do optymalizacji.
- **`HyperparameterOptimizer`** — Optymalizator hiperparametrów używający Langevin sampling.
- **`DeliveryPoint`** — Punkt dostawy.
- **`VRPSolver`** — Solver dla Vehicle Routing Problem.
- **`Surgery`** — Operacja do zaplanowania.
- **`OperatingRoom`** — Sala operacyjna.
- **`ORScheduler`** — Scheduler dla sal operacyjnych.
- **`PowerPlant`** — Elektrownia.
- **`UnitCommitmentSolver`** — Solver dla problemu Unit Commitment.
- **`GenomicSample`** — Próbka genomowa do analizy.
- **`PipelineStep`** — Krok w pipeline genomicznym.
- **`GenomicPipelineScheduler`** — Scheduler dla pipeline'u analizy genomowej.
- **`CoreIntegrator`** — Integrates Polish language support with NLP2CMD core system
- **`HighPriorityFixer`** — Implements high priority fixes for NLP2CMD system
- **`FinalAnalyzer`** — Analyzes the complete fix implementation and provides next steps
- **`ProjectSummary`** — Generates final project summary
- **`ComprehensiveTestFixer`** — Analyzes and fixes issues in comprehensive test results
- **`SimpleE2ETester`** — Simple E2E test runner for NLP2CMD service.

### Functions

- `print_status()` — —
- `print_success()` — —
- `print_warning()` — —
- `print_error()` — —
- `print_header()` — —
- `check_nlp2cmd()` — —
- `generate_command_schema()` — —
- `create_placeholder_schema()` — —
- `install_command_with_schema()` — —
- `run_nlp2cmd_command()` — —
- `test_all_commands()` — —
- `show_schemas()` — —
- `cleanup()` — —
- `main()` — —
- `print_status()` — —
- `print_success()` — —
- `print_warning()` — —
- `print_error()` — —
- `print()` — —
- `extract_domain()` — —
- `run()` — —
- `main()` — —
- `print_separator(title)` — —
- `print_rule()` — —
- `init_verbose(enabled)` — Initialize verbose mode. Call early, before importing nlp2cmd modules.
- `vlog(msg, indent)` — Print a verbose log message (only when --verbose is active).
- `dump_page_schema(page, max_depth)` — Inspect the page DOM and print a schema summary.
- `dump_selectors(page, selectors)` — Try each selector and report which ones matched elements.
- `vlog_decision(action, reason, alternatives)` — Log a decision made during automation.
- `ensure_playwright_browsers(auto_install, browser_type)` — Check if Playwright browsers are installed, and auto-install if missing.
- `ensure_playwright_browsers_async(auto_install, browser_type)` — Check if Playwright browsers are installed, and auto-install if missing.
- `discover_working_url(page, initial_url, fallback_urls, required_selector)` — Auto-discover working URL when initial URL fails (404 or missing required elements).
- `auto_navigate_with_fallback(page, target_urls, target_name)` — Navigate to target URL with automatic fallback discovery.
- `print_status()` — —
- `print_success()` — —
- `print_warning()` — —
- `print_error()` — —
- `check_script()` — —
- `run_python_script()` — —
- `show_usage()` — —
- `run_example()` — —
- `list_examples()` — —
- `main()` — —
- `main()` — —
- `example_scheduling()` — Example 1: Scheduling tasks with Langevin dynamics.
- `example_allocation()` — Example 2: Resource allocation with thermodynamic sampling.
- `example_energy_savings()` — Example 3: Energy savings estimation.
- `example_majority_voting()` — Example 4: Majority voting strategies.
- `example_routing()` — Example 5: Routing/TSP optimization with Langevin dynamics.
- `example_direct_problem()` — Example 6: Direct problem definition (without NL parsing).
- `main()` — Run all examples.
- `main()` — —
- `print_section(title)` — Print section header.
- `print_step(step)` — Print step indicator.
- `mock_sql_select(table, columns, filters)` — Mock SQL SELECT handler.
- `mock_shell_find(glob, path)` — Mock shell find handler.
- `mock_shell_count_pattern(file, pattern)` — Mock shell grep/count handler.
- `mock_k8s_get(resource, namespace)` — Mock kubectl get handler.
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `demo_intelligent_nlp2cmd()` — Demonstrate the intelligent NLP2CMD system.
- `demonstrate_persistent_storage()` — Demonstrate the persistent storage system.
- `show_storage_benefits()` — Show the benefits of per-command storage.
- `main()` — Run the enhanced NLP2CMD demo.
- `demonstrate_schema_flow()` — Demonstrate complete schema flow.
- `demonstrate_multiple_commands()` — Demonstrate with multiple commands.
- `show_schema_details()` — Show detailed schema information.
- `main()` — Main demonstration.
- `demonstrate_version_detection()` — Demonstrate practical version detection and command adaptation.
- `show_integration_example()` — Show how to integrate version detection into NLP2CMD.
- `show_version_mapping()` — Show version mapping for different commands.
- `main()` — Main demonstration.
- `show_schema_extraction_flow()` — Show how schema extraction works.
- `show_file_locations()` — Show where everything is stored.
- `show_api_usage()` — Show API usage examples.
- `main()` — Main function.
- `main()` — —
- `run_nlp2cmd_command(command, verbose)` — Run nlp2cmd with the given command.
- `get_command_for_service(service)` — Get natural language command for credential diagnosis.
- `main()` — —
- `check()` — —
- `run_flow(dry_run)` — —
- `main()` — —
- `main()` — —
- `scan()` — Pokaż tabelę dostępności credentials.
- `plan_all()` — Wygeneruj plany dla providerów z hasłami ale bez kluczy API.
- `setup_providers(providers)` — Wykonaj setup dla wybranych providerów.
- `setup_all()` — Setup dla wszystkich providerów z hasłami ale bez kluczy.
- `main()` — —
- `check_credentials()` — Sprawdź dostępność danych logowania.
- `run_flow(dry_run)` — Uruchom pełny flow pobierania klucza.
- `main()` — —
- `check()` — —
- `run_flow(dry_run)` — —
- `main()` — —
- `check()` — —
- `run_flow(dry_run)` — —
- `main()` — —
- `old_way_examples()` — Examples of old system usage patterns
- `new_way_examples()` — Examples of new TOON system usage
- `migration_steps()` — Step-by-step migration guide
- `performance_comparison()` — Performance comparison examples
- `practical_examples()` — Practical migration examples
- `main()` — Main migration guide
- `migrate_existing_schemas(source_file)` — Migrate existing schemas to versioned storage.
- `demonstrate_schema_updates(store)` — Demonstrate updating schemas with new versions.
- `demonstrate_dual_versions(store)` — Demonstrate handling two versions of the same command.
- `main()` — Main demonstration.
- `run_demo_with_test(interactive)` — Run demo with automatic deployment and testing.
- `test_services(controller)` — Test if services are working properly.
- `test_chat_service(container)` — Test chat service (nginx).
- `test_redis_service(container)` — Test Redis service.
- `troubleshoot_and_fix(controller, original_command)` — Troubleshoot and fix deployment issues.
- `interactive_mode(controller)` — Interactive mode for additional commands.
- `run_batch_demo()` — Run all commands from prompt.txt automatically.
- `test_services(controller)` — Test if services are working properly.
- `test_chat_service(container)` — Test chat service (nginx).
- `test_redis_service(container)` — Test Redis service.
- `test_postgres_service(container)` — Test PostgreSQL service.
- `demo_nlp_commands()` — Interaktywna demonstracja poleceń NLP.
- `run_example(example_num)` — Run specific example.
- `main()` — —
- `process_command(request)` — Przetwarzaj komendę z języka naturalnego.
- `get_status()` — Pobierz status API.
- `get_history(limit)` — Pobierz historię komend.
- `get_services()` — Pobierz wdrożone usługi.
- `home(request)` — Strona główna z interfejsem użytkownika.
- `history_page(request)` — Strona z historią komend.
- `services_page(request)` — Strona z usługami.
- `get_examples()` — Pobierz przykładowe komendy.
- `run_command(command, dsl, use_llm, auto_install)` — Quick way to run a single NLP2CMD command.
- `generate_compose(services)` — Generuje strukturę docker-compose.
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `benchmark_performance()` — Benchmark performance comparison
- `compare_usage_patterns()` — Compare usage patterns between old and new systems
- `compare_data_structure()` — Compare data structure differences
- `demonstrate_llm_friendly_format()` — Show how TOON format is LLM-friendly
- `main()` — Main demo function
- `main()` — Main demo function
- `demo_basic_usage()` — Demonstrate basic TOON usage
- `demo_real_world_example()` — Show real-world example
- `demo_integration_example()` — Show integration example
- `demo_advanced_features()` — Show advanced features
- `demo_performance_tips()` — Show performance tips
- `main()` — Main demo function
- `main()` — Demonstrate TOON usage
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `batch_validate(commands)` — Walidacja wsadowa komend.
- `batch_export(commands, format)` — Eksport wsadowy komend.
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `benchmark_old_system()` — Benchmark starego systemu.
- `benchmark_toon()` — Benchmark TOON - pojedynczy plik.
- `main()` — —
- `main()` — —
- `estimate_old_system_memory()` — Estymacja zużycia pamięci starego systemu.
- `estimate_toon_memory()` — Estymacja zużycia pamięci TOON.
- `format_size(size_bytes)` — Formatuje rozmiar w bajtach na czytelną formę.
- `main()` — —
- `mock_docker_ps()` — Mock: List Docker containers.
- `mock_k8s_get(resource)` — Mock: Get Kubernetes resources.
- `mock_sql_select(table)` — Mock: SQL query.
- `mock_process_list()` — Mock: System process list.
- `check_health(data)` — Custom handler: Analyze health status.
- `main()` — —
- `mock_find_logs()` — Mock: Find log files.
- `mock_count_pattern(file, pattern)` — Mock: Count pattern occurrences in file.
- `mock_read_file(path)` — Mock: Read file contents.
- `main()` — —
- `print_section(title)` — Print section header.
- `print_result(result, title)` — Print validation result.
- `main()` — —
- `print_section(title)` — Print section header.
- `run_single_command_benchmark(nlp, command)` — Run benchmark for a single command.
- `run_sequential_benchmark(nlp, commands)` — Run benchmark for sequential commands.
- `benchmark_adapters()` — Benchmark different adapters.
- `generate_report(results)` — Generate comprehensive benchmark report.
- `generate_markdown_report(report)` — Generate a comprehensive Markdown report with thermodynamic analysis.
- `save_report(report, filename)` — Save benchmark report to file.
- `print_report_summary(report)` — Print a summary of the benchmark report.
- `main()` — Main benchmark function.
- `print_section(title)` — Print section header.
- `run_command_with_timing(nlp, command)` — Run a single command and return the result with timing.
- `main()` — Demonstrate sequential command processing.
- `print_section(title)` — Print section header.
- `main()` — —
- `main()` — —
- `demonstrate_mock_llm()` — Demonstrate with mock LLM backend.
- `demonstrate_rule_based_fallback()` — Demonstrate with rule-based fallback.
- `demonstrate_real_llm_setup()` — Show how to set up real LLM backends.
- `demonstrate_hybrid_approach()` — Demonstrate hybrid LLM + rule-based approach.
- `main()` — Run all demonstrations.
- `main()` — —
- `main()` — —
- `main()` — —
- `format_size(gb)` — Format size in human-readable format.
- `main()` — —
- `simulate_interactive_session()` — Simulate an interactive session with feedback loop.
- `run_nlp2cmd_command(command, verbose)` — Run nlp2cmd with the given command.
- `get_command_for_task(task)` — Get natural language command for shell tasks.
- `main()` — —
- `main()` — —
- `main()` — —
- `run_nlp2cmd_command(command, verbose)` — Run nlp2cmd with the given command.
- `get_command_for_task(task)` — Get natural language command for Docker tasks.
- `main()` — —
- `create_sample_files(tmpdir)` — Create sample files for testing.
- `validate_file(registry, path, schema_name)` — Validate a file and print results.
- `repair_file(registry, path, schema_name, auto_fix)` — Repair a file and show changes.
- `main()` — —
- `main()` — —
- `show_help()` — —
- `check_nlp2cmd()` — —
- `Nlp2cmd()` — —
- `main()` — —
- `get_platform_info()` — Get platform info for logging and diagnostics.
- `dismiss_popups(page, log, timeout)` — Dismiss common popups, cookie banners, GDPR notices.
- `check_page_health(page, required_selector, log)` — Comprehensive page health check after navigation.
- `discover_working_url(page, site_name, custom_urls, required_selector)` — Intelligent URL discovery with fallback chain and health checks.
- `wait_for_canvas(page, selector, timeout_s, log)` — Poll for a visible canvas element up to timeout_s seconds.
- `retry_async(coro_fn, max_retries, backoff, log)` — Retry an async operation with exponential backoff.
- `find_canvas(page, log)` — Find the best canvas element using multiple strategies.
- `take_screenshot(page, path, log, metadata)` — Take a screenshot and save metadata alongside it.
- `main()` — —
- `map_vision_to_shapes(vision_description)` — Map vision analysis output to known shapes.
- `list_shapes(category)` — List all registered shapes organized by category.
- `generate_svg(shape_name, size)` — Generate SVG string for a single shape.
- `generate_svg_files(shapes)` — Generate individual SVG files for each shape.
- `generate_html_gallery(shapes)` — Generate HTML gallery page with all shapes.
- `analyze_image_and_draw(image_path, headless)` — Analyze image with Qwen VL via DrawValidationSkill and draw matching shapes.
- `draw_on_canvas(shapes, headless, title)` — Draw shapes in a grid on jspaint.app using 3-skill architecture.
- `main()` — —
- `main()` — —
- `mock_example_execution(context)` — Symuluje wykonanie przykładu z możliwością błędu.
- `run_scenario(scenario_name, use_orchestrator)` — Uruchamia scenariusz z lub bez orchestratora.
- `print_metrics_report(metrics, title)` — Drukuje raport metryk.
- `print_learning_report()` — Drukuje raport uczenia się.
- `main()` — —
- `parse_objects_from_scene(scene)` — Parse object names from a scene description.
- `run_scene(objects, headless, use_vision, verbose)` — Draw a multi-object scene using the 3-skill architecture.
- `show_database()` — Show all available shape sources.
- `main()` — —
- `search_demo(query, max_results, summarize)` — Demonstrate search functionality.
- `main()` — —
- `run_autonomous(description, headless, max_iterations, verbose)` — Run the full autonomous drawing pipeline using 3 skills.
- `fetch_only(shape_name)` — Just fetch a shape from databases and display info.
- `main()` — —
- `run_nlp2cmd_command(command, headless, verbose)` — Run nlp2cmd with the given command.
- `get_command_for_shape_and_color(shape, color)` — Get natural language command for drawing shapes.
- `get_fallback_command(shape, color)` — Get fallback command for when draw.chat is down (based on analysis).
- `main()` — —
- `main()` — —
- `main()` — —
- `resolve_shapes(description, verbose)` — Resolve shape names from description.
- `run_autonomous(description, headless, max_corrections, verbose)` — Run the full autonomous drawing pipeline.
- `fetch_only(shape_name)` — Just fetch a shape from databases and display info.
- `main()` — —
- `run_nlp2cmd_command(command, headless, verbose)` — Run nlp2cmd with the given command.
- `get_command_for_pattern_and_color(pattern, color, fallback)` — Get natural language command for painting patterns.
- `get_pattern_analysis_info()` — Get pattern painting information based on analysis.
- `main()` — —
- `run_nlp2cmd_command(command, headless, verbose)` — Run nlp2cmd with the given command.
- `get_adaptive_command(prompt, fallback)` — Get adaptive drawing command based on analysis findings.
- `get_color_analysis_info()` — Get color handling information based on analysis.
- `main()` — —
- `run_nlp2cmd_command(command, headless, verbose)` — Run nlp2cmd with the given command.
- `main()` — —
- `generate_plan_with_llm(query)` — Try to generate a drawing plan using LLM Router with adaptive learning.
- `main()` — —
- `main()` — —
- `draw_and_validate(shape, color, description, headless)` — Draw a shape using 3-skill pipeline and validate with Qwen VL.
- `validate_screenshot(screenshot_path, description, verbose, use_vision)` — Validate an existing screenshot without drawing.
- `run_demo(headless, use_vision)` — Run validation on multiple demo scenarios.
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `should_run()` — —
- `main()` — —
- `main()` — —
- `run_nlp2cmd_command(command, headless, verbose)` — Run nlp2cmd with the given command.
- `main()` — —
- `run_nlp2cmd_command(command, headless, verbose)` — Run nlp2cmd with the given command.
- `get_command_for_preset(preset)` — Get natural language command for a preset.
- `main()` — —
- `main()` — —
- `main()` — —
- `detect_language(query)` — Detect programming language from query.
- `detect_task(query)` — Detect coding task from query keywords.
- `generate_code_with_llm(query, lang)` — Generate code using LLM Router with adaptive learning.
- `main()` — —
- `run_nlp2cmd_command(command, headless, verbose)` — Run nlp2cmd with the given command.
- `get_command_for_code(code, lang)` — Get natural language command for code execution.
- `main()` — —
- `run_nlp2cmd_command(command, headless, verbose)` — Run nlp2cmd with the given command.
- `get_command_for_preset(preset)` — Get natural language command for a preset.
- `main()` — —
- `type_into_codepen_editor(page, panel_selector, code)` — Type code into a CodePen editor panel using CodeMirror API.
- `generate_code_from_description(description)` — Generate simple HTML/CSS/JS from natural language description.
- `main()` — —
- `json_safe(s)` — Escape string for safe JS injection.
- `run_nlp2cmd_command(command, headless, verbose)` — Run nlp2cmd with the given command.
- `main()` — —
- `build_prompt(args)` — Build the full prompt from CLI arguments.
- `main()` — —
- `run_benchmark(validator, runs_per_case, label)` — Run benchmark: each case N times, collect accuracy/consistency/latency.
- `compare_benchmarks(before, after)` — Print comparison of two benchmark runs.
- `main()` — —
- `test_prompt(example, verbose)` — Test a single prompt against ActionPlanner (dry-run, no browser).
- `run_all_tests(provider, verbose)` — Run all prompt tests and return summary.
- `print_separator(title)` — —
- `print_rule()` — —
- `rule_line()` — —
- `print_demo_header(title)` — —
- `run_thermo_demo(title, prompt)` — —
- `print_metrics(result)` — —
- `print_simple_result(query, result, elapsed_ms)` — —
- `print_full_result(query, result, elapsed_ms)` — —
- `sigmoid(value)` — —
- `project_sample(problem, raw_sample)` — —
- `print_projected(title, projected)` — —
- `print_fallback_note(problem_name)` — —
- `run_all_demos()` — Uruchom wszystkie demonstracje.
- `print_summary_table()` — Wyświetl tabelę podsumowującą zastosowania.
- `test_polish_queries()` — Test Polish language queries with mock LLM.
- `test_integration_pattern()` — Test the integration pattern for real LLM.
- `show_real_setup_instructions()` — Show instructions for real model setup.
- `download_bielik()` — Pobierz model Bielik-1.5B GGUF.
- `main()` — Główna funkcja setup.
- `test_pdf_search_queries()` — Test różnych zapytań o wyszukiwanie PDF.
- `show_configuration_guide()` — Pokaż przewodnik konfiguracji.
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `demo_unit_commitment()` — Harmonogramowanie pracy elektrowni (Unit Commitment).
- `demo_renewable_integration()` — Integracja OZE z siecią.
- `demo_water_distribution()` — Optymalizacja sieci wodociągowej.
- `demo_gas_network()` — Optymalizacja sieci gazowej.
- `demo_electric_vehicle_charging()` — Zarządzanie stacjami ładowania EV.
- `demo_demand_response()` — Programy Demand Response.
- `demo_microgrid()` — Optymalizacja mikrosieci.
- `main()` — Uruchom wszystkie demonstracje energetyczne.
- `demo_lead_optimization()` — Optymalizacja leadu z ograniczeniami fizykochemicznymi.
- `demo_admet_balancing()` — Wielokryterialna optymalizacja ADMET.
- `main()` — Uruchom demonstracje Drug Discovery.
- `demo_vehicle_routing()` — Optymalizacja tras dostaw (VRP).
- `demo_warehouse_optimization()` — Optymalizacja rozmieszczenia produktów w magazynie.
- `demo_production_scheduling()` — Harmonogramowanie produkcji.
- `demo_inventory_optimization()` — Optymalizacja zapasów.
- `demo_supply_chain_network()` — Optymalizacja sieci łańcucha dostaw.
- `demo_cross_docking()` — Optymalizacja cross-docking.
- `main()` — Uruchom wszystkie demonstracje logistyczne.
- `print_result(query, result, elapsed)` — Helper function to print results for both DSL and Thermodynamic sources.
- `run_query_group(title, section_label, queries)` — —
- `demo_file_operations()` — Demonstracja operacji na plikach.
- `demo_system_monitoring()` — Demonstracja monitoringu systemu.
- `demo_network_operations()` — Demonstracja operacji sieciowych.
- `demo_process_management()` — Demonstracja zarządzania procesami.
- `demo_development_tools()` — Demonstracja narzędzi deweloperskich.
- `demo_security_operations()` — Demonstracja operacji bezpieczeństwa.
- `demo_backup_operations()` — Demonstracja operacji backup.
- `demo_system_maintenance()` — Demonstracja konserwacji systemu.
- `main()` — Uruchom wszystkie demonstracje komend DSL.
- `demo_hyperparameter_optimization()` — Optymalizacja hiperparametrów modelu ML.
- `demo_feature_selection()` — Optymalizacja wyboru cech dla modelu ML.
- `demo_experiment_scheduling()` — Planowanie eksperymentów ML na klastrze GPU.
- `demo_model_ensemble_optimization()` — Optymalizacja ensemble modeli.
- `main()` — Uruchom wszystkie demonstracje Data Science.
- `demo_traffic_optimization()` — Optymalizacja sygnalizacji świetlnej.
- `demo_smart_grid()` — Bilansowanie obciążenia sieci energetycznej.
- `demo_waste_management()` — Optymalizacja tras wywozu odpadów.
- `demo_public_transport()` — Optymalizacja transportu publicznego.
- `demo_parking_management()` — Zarządzanie parkingami.
- `demo_air_quality()` — Monitorowanie i optymalizacja jakości powietrza.
- `demo_water_management()` — Zarządzanie systemem wodociągowym.
- `main()` — Uruchom wszystkie demonstracje smart cities.
- `demo_portfolio_optimization()` — Optymalizacja portfela inwestycyjnego (Markowitz).
- `demo_trade_execution()` — Optymalizacja wykonania dużego zlecenia (TWAP/VWAP).
- `demo_risk_allocation()` — Alokacja limitów ryzyka między deskami tradingowymi.
- `demo_arbitrage_detection()` — Wykrywanie i optymalizacja arbitrażu.
- `demo_options_strategy()` — Optymalizacja strategii opcji.
- `demo_credit_scoring()` — Optymalizacja modeli credit scoring.
- `main()` — Uruchom wszystkie demonstracje finansowe.
- `demo_particle_collision()` — Planowanie eksperymentów w akceleratorze cząstek.
- `demo_molecular_dynamics()` — Optymalizacja parametrów symulacji MD.
- `demo_telescope_scheduling()` — Harmonogram obserwacji teleskopowych.
- `demo_quantum_computing()` — Optymalizacja obwodów kwantowych.
- `demo_climate_modeling()` — Optymalizacja parametrów modelu klimatu.
- `demo_particle_physics()` — Analiza danych z fizyki cząstek.
- `demo_materials_science()` — Optymalizacja eksperymentów materiałoznawstwa.
- `main()` — Uruchom wszystkie demonstracje fizyki.
- `demo_or_scheduling()` — Harmonogramowanie sal operacyjnych.
- `demo_nurse_scheduling()` — Grafik dyżurów pielęgniarek.
- `demo_patient_allocation()` — Alokacja pacjentów do ramion badania klinicznego.
- `demo_emergency_department()` — Optymalizacja pracy oddziału ratunkowego.
- `demo_ambulance_dispatch()` — Dyspozycja karetek pogotowia.
- `demo_icu_bed_management()` — Zarządzanie łóżkami na OIOM.
- `demo_pharmacy_inventory()` — Zarządzanie zapasami w aptece szpitalnej.
- `main()` — Uruchom wszystkie demonstracje healthcare.
- `demo_devops_commands()` — Podstawowe komendy DevOps.
- `demo_ci_cd_optimization()` — Optymalizacja CI/CD Pipeline.
- `demo_incident_response()` — Automatyczna analiza i response na incydenty.
- `main()` — Uruchom wszystkie demonstracje DevOps.
- `demo_genomic_pipeline()` — Optymalizacja pipeline'u analizy genomowej.
- `demo_protein_folding()` — Alokacja zasobów dla symulacji foldingu białek.
- `demo_crispr_optimization()` — Optymalizacja sekwencji guide RNA.
- `demo_proteomics_analysis()` — Planowanie analizy proteomicznej.
- `demo_drug_discovery()` — Optymalizacja procesu odkrywania leków.
- `main()` — Uruchom wszystkie demonstracje bioinformatyki.
- `print_separator(title)` — Drukuj ładny separator z tytułem.
- `print_result(query, result, elapsed, source)` — Wyświetl wynik w standardowym formacie.
- `demo_python_api()` — Demonstracja użycia Python API.
- `demo_shell_commands()` — Demonstracja komend shell.
- `demo_mixed_usage()` — Demonstracja mieszanego użycia Python + shell.
- `demo_advanced_features()` — Demonstracja zaawansowanych funkcji.
- `main()` — Główna funkcja demonstracyjna.
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `debug_keywords()` — Debug keyword patterns.
- `debug_generator()` — Debug generator internals.
- `main()` — Uruchom walidację komend shell.
- `debug_intents()` — Debug intent detection.
- `print_separator(title)` — Drukuj separator z tytułem.
- `demo_python_api_concept()` — Demonstracja koncepcji Python API.
- `demo_shell_commands()` — Demonstracja komend shell.
- `demo_mixed_workflow()` — Demonstracja mieszanego workflow.
- `demo_advanced_patterns()` — Demonstracja zaawansowanych wzorców.
- `demo_real_world_examples()` — Demonstracja rzeczywistych przypadków użycia.
- `main()` — Główna funkcja demonstracyjna.
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `main()` — —
- `demo_course_timetabling()` — Układanie planu zajęć na uczelni.
- `demo_exam_scheduling()` — Harmonogram sesji egzaminacyjnej.
- `demo_learning_path()` — Personalizacja ścieżki nauki.
- `demo_classroom_allocation()` — Alokacja sal wykładowych.
- `demo_student_grouping()` — Tworzenie grup projektowych.
- `demo_resource_optimization()` — Optymalizacja zasobów edukacyjnych.
- `demo_curriculum_planning()` — Planowanie programu nauczania.
- `main()` — Uruchom wszystkie demonstracje edukacyjne.
- `ollama_available()` — —
- `ollama_model_exists(name)` — —
- `ollama_create_bielik()` — Create ollama model from local Bielik GGUF if not already present.
- `ollama_generate(model, prompt, system, max_tokens)` — Call ollama /api/generate, return (text, duration_sec).
- `clean_command(raw)` — Extract clean command from LLM response.
- `run_benchmark()` — —
- `build_summary(results)` — Aggregate per-model and per-domain stats.
- `generate_html(results)` — Generate interactive HTML with Chart.js visualisations.
- `print_summary(results)` — —
- `generate_refactoring_notes(results)` — Generate refactoring recommendations based on benchmark data.
- `generate_command_errors_report(results)` — Generate a Markdown report listing incorrect commands.
- `main()` — —
- `benchmark_langevin_sampler(n_iterations, n_steps, dim)` — Benchmark raw Langevin sampler performance.
- `benchmark_parallel_vs_sequential(n_samples, n_steps, dim)` — Compare parallel vs sequential sampling.
- `benchmark_adaptive_steps(problem_sizes)` — Benchmark adaptive steps for different problem sizes.
- `benchmark_generator_problems(n_iterations)` — Benchmark different problem types with ThermodynamicGenerator.
- `benchmark_energy_savings()` — Calculate energy savings for different scenarios.
- `print_benchmark_result(result)` — Pretty print a benchmark result.
- `main()` — Run all benchmarks.
- `run_learning_benchmark()` — —
- `generate_html(results)` — —
- `print_summary(results)` — —
- `main()` — —
- `get_timestamp()` — Generate timestamp string for filenames.
- `ensure_dir(path)` — Ensure directory exists, create if not.
- `ask_for_screenshot(console, default_path)` — Ask user if they want to take a screenshot.
- `take_screenshot(page, path, console)` — Take a screenshot of current page state.
- `ask_for_video_recording(console)` — Ask user if they want to record video.
- `get_polish_support()` — Get Polish language support instance
- `load_appspec(path)` — —
- `get_monitor()` — Get the global resource monitor instance.
- `measure_resources()` — Convenient context manager for resource measurement.
- `get_last_metrics()` — Get metrics from last execution.
- `format_last_metrics()` — Format metrics from last execution for display.
- `get_system_info()` — Get general system information.
- `estimate_token_cost(time_ms, cpu_percent, memory_mb, energy_mj)` — Convenient function for token cost estimation.
- `format_token_estimate(estimate)` — Format token cost estimate for display.
- `parse_metrics_string(metrics_str)` — Parse metrics string like '⏱️ Time: 2.6ms | 💻 CPU: 0.0% | 🧠 RAM: 53.5MB (0.1%) | ⚡ Energy: 0.022mJ'
- `lookup_blueprint(query)` — Find a matching drawing blueprint for the given query.
- `get_blueprint_steps(query)` — Get drawing steps for a matched blueprint.
- `list_available_blueprints()` — Return list of available blueprint names.
- `get_password_store()` — Get the singleton password store instance.
- `get_vector_store(persist_dir)` — Get or create the global vector store instance.
- `initialize_default_patterns()` — Initialize vector store with default drawing patterns.
- `export_patterns_to_file(filepath)` — Export all patterns to a JSON file for backup/sharing.
- `import_patterns_from_file(filepath)` — Import patterns from a JSON file.
- `create_optimized_matcher_from_phrases(phrases_path, preload)` — Create an OptimizedSemanticMatcher from phrases JSON.
- `get_optimized_semantic_matcher(preload)` — Get or create optimized semantic matcher singleton.
- `preload_models()` — Pre-load all models at application startup.
- `clear_embedding_cache()` — Clear the embedding cache to free memory.
- `get_cache_stats()` — Get embedding cache statistics.
- `fingerprint(text)` — Create a stable fingerprint for a query (lowercase, stripped, hashed).
- `fuzzy_fingerprint(text)` — Create a looser fingerprint ignoring stop words and punctuation.
- `detect_domain(text)` — Detect domain from keywords. Returns best match or 'shell' as default.
- `load_expanded_phrases(path)` — Load samples from expanded_phrases.json.
- `load_patterns(path)` — Load samples from patterns.json.
- `load_command_schemas(schemas_dir)` — Load samples from command schema files.
- `generate_augmented_samples(samples)` — Generate augmented training samples with variations.
- `deduplicate_samples(samples)` — Remove duplicate samples.
- `train_all_models(data_dir, output_dir, augment, verbose)` — Train ML models on all available data.
- `quick_test(data_dir)` — Quick test of trained model.
- `create_multilingual_matcher(phrases_dict, schema_path)` — Create a fuzzy matcher with default multilingual phrases.
- `should_attempt_repair(error, context)` — Determine if auto-repair should be attempted.
- `create_thermodynamic_generator(n_samples, n_steps, adaptive_steps, parallel_sampling)` — Create a thermodynamic generator with default configuration.
- `generate_training_data_from_phrases(phrases_path)` — Generate training data from multilingual_phrases.json.
- `create_default_training_data()` — Create default training dataset for shell commands.
- `get_ml_classifier(force_retrain)` — Get or create ML intent classifier singleton.
- `get_multi_command_detector()` — Get or create the global multi-command detector instance.
- `detect_multi_commands(text)` — Convenience function to detect multiple commands.
- `get_enhanced_detector()` — Get or create enhanced detector instance.
- `load_legacy_phrases(path)` — Load phrases from legacy multilingual_phrases.json format.
- `merge_databases()` — Merge multiple phrase databases.
- `benchmark_formats(db, iterations)` — Benchmark different data formats.
- `create_pipeline(confidence_threshold, custom_patterns)` — Create a RuleBasedPipeline with default configuration.
- `create_default_validators()` — Create default validators for all domains.
- `create_hybrid_generator(llm_client, confidence_threshold)` — Factory function to create a hybrid generator.
- `add_service_command(main_group)` — Add service command to the main CLI group.
- `create_app()` — Create FastAPI application for uvicorn import.
- `create_service_config_from_args(host, port, debug, log_level)` — Create ServiceConfig from command line arguments.
- `get_data_manager(toon_file)` — Get or create data manager instance
- `reload_data_manager(toon_file)` — Reload data manager with new file
- `load_command_schemas()` — Load command schemas (backward compatibility)
- `load_config()` — Load configuration (backward compatibility)
- `get_project_info()` — Get project information (backward compatibility)
- `get_service_registry(config_dir)` — Return the global ServiceRegistry singleton (lazy-loaded).
- `get_intent_registry(config_dir)` — Return the global IntentRegistry singleton (lazy-loaded).
- `detect_language(text)` — Heuristic language detection based on character sets and word frequency.
- `normalize_unicode(text)` — Apply NFC normalization so combining characters are composed.
- `fold_accents(text)` — Strip diacritical marks, producing ASCII-like text for fuzzy matching.
- `correct_typos(text, threshold)` — Correct known typos in *text* using direct lookup + rapidfuzz fallback.
- `tokenize(text)` — Split *text* into tokens suitable for downstream NLP processing.
- `test_per_command_store()` — Test the per-command schema store.
- `demonstrate_version_management()` — Demonstrate version management for command schemas.
- `web_schema_group()` — Web schema extraction and management commands.
- `extract_schema(url, output, headless)` — Extract schema from a web page.
- `show_history(domain, limit, stats)` — Show interaction history.
- `export_learned_schema(domain, output)` — Export learned schema from interaction history.
- `clear_history(domain, clear_all)` — Clear interaction history.
- `display_command_result(command, metadata, metrics_str, show_yaml)` — Display command result with simple YAML format and bash markdown.
- `display_table(data, title, headers, show_headers)` — Display data in a formatted table.
- `display_panel(content, title, border_style, padding)` — Display content in a formatted panel.
- `display_info(message, style)` — Display informational message.
- `display_success(message)` — Display success message.
- `display_error(message)` — Display error message.
- `display_warning(message)` — Display warning message.
- `display_debug(message)` — Display debug message.
- `display_progress(message, spinner)` — Display progress message.
- `display_section(title, content)` — Display section with title and optional content.
- `display_list(items, title, bullet)` — Display list of items.
- `display_kv_pairs(data, title, indent)` — Display key-value pairs.
- `get_adapter(dsl, context)` — Get the appropriate adapter for the DSL type.
- `with_auto_repair(auto_confirm, console)` — Decorator that adds auto-repair capability to any function.
- `execute_with_auto_recovery(func)` — Execute a function with automatic error recovery.
- `get_syntax_cache()` — Get the global syntax cache instance.
- `get_cached_syntax(code, lexer, theme, line_numbers)` — Get a cached Syntax object using the global cache.
- `clear_syntax_cache()` — Clear the global syntax cache.
- `get_cache_stats()` — Get global cache statistics.
- `print_markdown_block(renderable)` — Print a renderable or string wrapped in a Markdown code block.
- `print_yaml_block(data)` — —
- `history_group()` — Command history and analytics.
- `show_history(dsl, limit, failed_only)` — Show command execution history.
- `show_stats(schema_usage)` — Show command execution statistics.
- `show_popular(limit)` — Show most popular queries.
- `export_analytics(output)` — Export detailed analytics to JSON.
- `clear_history(confirm)` — Clear command history.
- `repair(ctx, file, backup)` — Repair a configuration file.
- `validate(ctx, file)` — Validate a configuration file.
- `analyze_env(ctx, output)` — Analyze system environment.
- `version()` — —
- `main(ctx, interactive, dsl, appspec)` — NLP2CMD - Natural Language to Domain-Specific Commands.
- `cli_entry_point()` — Entry point that handles natural language queries before Click.
- `show_schema_info(console)` — Show available schemas (intents, entities, templates) as markdown.
- `show_decision_tree_info(query, console)` — Show decision tree for a query - step by step pipeline decisions.
- `generate_debug_log_md(query, output_path)` — Generate comprehensive debug log in markdown format.
- `cache_group()` — External dependencies cache management.
- `setup_cache(cache_dir)` — Setup environment for cached external dependencies.
- `install_package(package, force, cache_dir)` — Install external packages to cache.
- `show_cache_info(cache_dir)` — Show cache information and statistics.
- `check_cache(package, cache_dir)` — Check if packages are cached.
- `clear_cache(package, clear_all, cache_dir)` — Clear cached packages.
- `full_clear_cache(include_models, include_global_playwright)` — Clear all nlp2cmd caches (runtime + external + schema + optional global caches).
- `auto_setup(cache_dir)` — Automatically setup and install if needed.
- `cmd_repair(file, backup)` — Repair a configuration file.
- `cmd_validate(file)` — Validate a configuration file.
- `cmd_analyze_env(output)` — Analyze system environment.
- `run_doctor(auto_fix, output_json, fix_script)` — Run the doctor diagnostic.
- `get_hf_token_via_browser(console)` — Open browser to help user get HF_TOKEN from Hugging Face.
- `handle_generate_query(query)` — Handle single-query generation (no --run, dsl=auto fast path).
- `handle_appspec_query(query)` — Handle single-query generation for appspec DSL.
- `handle_run_mode(query, dsl, appspec, auto_confirm)` — Handle --run option: generate and execute command with error recovery.
- `quick_find_content(url, content_type, search_term, headless)` — Quick helper to find content URL without managing browser.
- `quick_find_form(url, intent, headless)` — Quick helper to find form URL without managing browser.
- `create_example_env_file(path)` — Create example .env file with form field templates.
- `create_example_form_data_json(path)` — Create example form_data.json file.
- `extract_web_schema(url, output_dir, headless, use_cache)` — Extract schema from a web page and optionally save it.
- `get_os_open_command()` — Get the appropriate command to open URLs on current OS.
- `normalize_url(url)` — Normalize a URL by adding protocol if missing.
- `open_url(url, use_webbrowser)` — Open a URL in the default browser.
- `search_web(query, engine)` — Search the web using the specified search engine.
- `generate_shell_command(action, params)` — Generate a shell command for browser actions.
- `create_default_registry(shell_policy, safety_policy)` — Create an ExecutorRegistry pre-loaded with all built-in executors.
- `explore(root, intent, search_term, space_type)` — Universal exploration function.
- `quick_find_file(path, pattern, max_depth)` — Quick helper to find file path.
- `quick_find_in_data(data, search_term, max_depth)` — Quick helper to find path in data.
- `get_resource_discovery_manager()` — Get or create the global resource discovery manager.
- `quick_find_endpoint(base_url, search_term, auth_token)` — Quick helper to find API endpoint URL.
- `classify_task(prompt)` — Classify prompt into task category using keyword patterns.
- `get_router()` — Get or create the default LLMRouter singleton.
- `reset_router()` — Reset the default router (e.g., after config change).
- `classify_error(error_msg, model, task)` — Classify an error message into a known pattern category.
- `parse_svg_path(d, scale, center)` — Parse SVG path 'd' attribute into point groups.
- `validate_geometry(points, name)` — Validate generated geometry for common issues.
- `normalize_points(points, target_size)` — Normalize point groups to fit within [-target_size, target_size] centered at origin.
- `get_registry()` — Get the global action registry instance.
- `get_workspace()` — Return the .nlp2cmd workspace directory, creating it if needed.
- `handle_shell_exec(step, ctx)` — Execute a shell command.
- `handle_generate_code(step, ctx)` — Generate code via LLM.
- `handle_wait(step, ctx)` — Wait for a specified duration.
- `handle_inspect(step, ctx)` — Inspect page DOM structure and store schema in context.
- `handle_navigate(step, ctx)` — Navigate browser page to URL.
- `handle_dismiss_popups(step, ctx)` — Dismiss cookie banners, consent dialogs, etc.
- `handle_inject_code(step, ctx)` — Inject code into a web page editor (CM5/CM6/Monaco/Ace/textarea).
- `handle_find_and_click(step, ctx)` — Find and click a button by purpose.
- `handle_capture_output(step, ctx)` — Capture program output from web page.
- `handle_screenshot(step, ctx)` — Take a screenshot.
- `handle_validate(step, ctx)` — Validate output via reflection (delegates to ResultAnalyzer).
- `handle_discover_url(step, ctx)` — Discover a working URL when the primary one fails (404, no canvas, etc.).
- `handle_check_health(step, ctx)` — Check page health: is the page loaded, has expected elements, no errors.
- `handle_find_canvas(step, ctx)` — Find and activate a canvas element on the page.
- `handle_draw_shape(step, ctx)` — Draw a shape on canvas using the DrawingSkill system.
- `handle_navigate_with_fallback(step, ctx)` — Navigate to URL with automatic fallback discovery if primary URL fails.
- `register_default_handlers(orch)` — Register all default step handlers on an Orchestrator instance.
- `has_error_signals(text)` — Fast check: does the text contain error patterns?
- `classify_error(text)` — Classify an error from output text (fast, no LLM).
- `suggest_retry_strategy(error_type)` — Suggest a retry strategy based on error classification.
- `is_playwright_installed()` — Check if Playwright is installed.
- `is_playwright_browsers_installed()` — Check if Playwright browsers are installed by looking for the executable.
- `install_playwright(console)` — Install Playwright package.
- `install_playwright_browsers(console)` — Install Playwright browsers (chromium).
- `ensure_playwright_installed(console, auto_install)` — Ensure Playwright is installed, prompting user if needed.
- `main()` — CLI interface for cache manager.
- `get_user_config_dir()` — Return the user config directory for NLP2CMD.
- `find_data_files()` — Return a list of existing data file paths in merge order.
- `find_data_file()` — Resolve a data/*.json file path.
- `data_file_write_path()` — Resolve a writable path for a data file.
- `parse_source_uri(uri)` — Parse a --source URI string into SourceURI.
- `create_enhanced_nlp2cmd(appspec_path, nlp_backend, config)` — —
- `get_parser(file_path)` — Get or create parser instance
- `reload_parser(file_path)` — Reload parser with new file
- `get_global_history()` — Get or create global command history instance.
- `record_command(query, dsl, command)` — Convenience function to record to global history.
- `register_action(action_name)` — Decorator to register a handler class.
- `get_action(action_name)` — Get the handler class for an action name.
- `register_handler(action_name)` — Decorator to register a handler class.
- `get_handler(action_name)` — Get the handler class for an action name.
- `test_dynamic_generation()` — Test dynamic schema generation.
- `test_command_detector()` — Test the command detector with various queries.
- `test_version_aware_generation()` — Test the version-aware command generation.
- `main(target, source_type, out_format, raw)` — —
- `validate_app2schema_export(payload)` — —
- `validate_appspec(payload)` — —
- `discover_openapi_spec_url(base_url)` — —
- `extract_schema(target)` — —
- `extract_appspec_to_file(target, out_path)` — —
- `extract_schema_to_file(target, out_path)` — —
- `ensure_playwright()` — Ensure playwright is available.
- `start_recording(container, duration)` — Start ffmpeg video recording inside the Docker container.
- `stop_recording(container)` — Stop ffmpeg recording.
- `run_demo()` — Run the desktop GUI automation demo with markdown session logging.
- `main()` — —
- `main()` — Demonstrate comprehensive command scanning.
- `main()` — Demonstrate non-LLM schema extraction.
- `load_commands_from_files()` — Load unique commands from cmd.csv and cmd.txt.
- `update_all_schemas(force_update)` — Update schemas for all commands.
- `main()` — Main function.
- `main()` — Demonstrate enhanced schema generation.
- `main()` — Main function to generate schemas for all commands.
- `main()` — Main entry point.
- `validate_and_fix_schemas()` — Validate all schemas and fix issues.
- `main()` — Demonstrate intelligent command generation.
- `create_enhanced_prompt_list()` — Create an enhanced list of test prompts.
- `main()` — Main function to generate CSV from prompt.txt.
- `load_prompts(prompt_file)` — Load prompts from file or create default list.
- `detect_command_version(command)` — Detect version of a command.
- `generate_command(prompt)` — Generate command from prompt using simple patterns.
- `main()` — Generate cmd.csv from prompt.txt.
- `analyze_version_standards()` — Analyze common version detection standards.
- `test_version_detection_patterns()` — Test various version detection patterns.
- `check_schema_version_support()` — Check if schemas have version detection implemented.
- `demonstrate_version_detection_implementation()` — Show how version detection is implemented.
- `best_practices()` — Show best practices for version detection.
- `main()` — Main analysis function.
- `compare_schemas()` — Compare schemas generated with and without LLM.
- `compare_batch_files()` — Compare results from batch files.
- `quick_test()` — Quick test of NLP2CMD command generation.
- `main()` — Setup external dependencies cache.
- `bump_version(version_type)` — Bump version in pyproject.toml
- `echo_info()` — —
- `echo_success()` — —
- `echo_warning()` — —
- `echo_error()` — —
- `main()` — —
- `main()` — —
- `demo_hybrid()` — Demonstracja generatora hybrydowego.
- `demo_thermodynamic()` — Demonstracja generatora termodynamicznego.
- `demo_complete_hybrid()` — Demonstracja pełnego generatora hybrydowego.
- `main()` — Główna funkcja demonstracyjna.
- `demo_hybrid()` — Demonstracja generatora hybrydowego.
- `demo_thermodynamic_improved()` — Demonstracja POPRAWIONEGO generatora termodynamicznego.
- `demo_hybrid_thermodynamic_improved()` — Demonstracja POPRAWIONEGO hybrydowego generatora.
- `benchmark_latency()` — Benchmark porównujący latencję przed/po poprawkach.
- `main()` — Główna funkcja demonstracyjna.
- `demo_devops_automation()` — Demonstracja automatyzacji DevOps.
- `demo_hyperparameter_optimization()` — Demonstracja optymalizacji hiperparametrów.
- `demo_vehicle_routing()` — Demonstracja optymalizacji tras dostaw.
- `demo_or_scheduling()` — Demonstracja harmonogramowania sal operacyjnych.
- `demo_unit_commitment()` — Demonstracja harmonogramowania elektrowni.
- `demo_genomic_pipeline()` — Demonstracja harmonogramowania pipeline'u genomicznego.
- `main()` — Uruchom wszystkie demonstracje.
- `main()` — Main integration function
- `main()` — Main function to apply all fixes
- `main()` — Main analysis function
- `apply_refactor_to_keyword_detector()` — Apply the refactored _detect_normalized method to KeywordIntentDetector.
- `print_summary()` — Print a summary of the refactoring work completed.
- `restore_core()` — Restore core.py from backup
- `restore_adapters()` — Restore adapters from backups
- `verify_restoration()` — Verify system restoration
- `main()` — Main restoration function
- `apply_core_patch()` — Apply core patch
- `apply_adapter_patches()` — Apply adapter patches
- `verify_integration()` — Verify integration
- `main()` — Main integration function
- `apply_keywords_refactor()` — Apply refactor to keywords.py file.
- `apply_templates_refactor()` — Apply refactor to templates.py file.
- `main()` — Main function to apply refactors.
- `load_polish_patterns()` — Load Polish shell patterns
- `load_intent_mappings()` — Load Polish intent mappings
- `load_table_mappings()` — Load Polish table mappings
- `load_domain_weights()` — Load domain weights
- `apply_fixes()` — Apply all fixes to the system
- `find_line(pattern, start)` — —
- `write_mixin(filename, classname, docstring, body_lines)` — Write a mixin file. body_lines are already indented with 4 spaces (class methods).
- `apply_to_keywords_py()` — Apply refactor to keywords.py file.
- `apply_to_templates_py()` — Apply refactor to templates.py file.
- `create_patch_files()` — Create patch files for manual application.
- `main()` — Main function to apply refactors.
- `build_parser()` — —
- `git_tracked_python_files(workdir)` — Return tracked Python files from the git repository.
- `select_llx_model(workdir)` — Select a model using LLX's project metrics and routing logic.
- `build_prompt(workdir, metrics, file_count)` — Build a refactor prompt for Aider.
- `run_refactor(workdir, model, prompt, use_docker)` — —
- `main()` — —
- `generate_refactor_report()` — Generate a detailed report of the refactoring work.
- `apply_refactor_to_template_generator()` — Apply the refactored _apply_shell_intent_specific_defaults method.
- `main()` — Main summary function
- `main()` — Apply all refactors and report results.
- `main()` — Main entry point.
- `main(argv)` — —
- `image_similarity(img1, img2)` — Oblicza podobieństwo między dwoma obrazami (0-100%).
- `detect_changes(folder)` — Wykrywa zmiany między kolejnymi zrzutami ekranu.
- `create_diff_images(folder, output_folder)` — Tworzy obrazy różnic między kolejnymi zrzutami.
- `main()` — —
- `log()` — —
- `log_success()` — —
- `log_error()` — —
- `log_warning()` — —
- `calculate_file_hash(filepath)` — Oblicza hash MD5 pliku.
- `analyze_screenshots(folder)` — Analizuje zrzuty ekranu w podanym folderze.
- `resize_screenshots(folder, scale_factor)` — Zmniejsza zrzuty ekranu o podany czynnik (domyślnie 30%).
- `main()` — Główna funkcja.


## Project Structure

📄 `.markdownlint`
📄 `CHANGELOG`
📄 `CONTRIBUTING`
📄 `Dockerfile`
📄 `INSTALLATION`
📄 `Makefile`
📄 `README`
📄 `REPO_SPLIT`
📄 `THERMODYNAMIC_ARCHITECTURE`
📄 `THERMODYNAMIC_INTEGRATION`
📄 `TODO`
📄 `TODO.chciałbym aby moja aplikacja realziowała złożone r`
📄 `TODO.co można zrobić z tego typu hardkodowanymi zmienny`
📄 `TODO.skad pobrac np 1000 takich obiektow, albo jeden pl`
📄 `TODO.skąd wziąć dane weektorowej postaci obeiktow jak z`
📄 `artifacts.benchmark_report`
📄 `artifacts.ci_test_results`
📄 `artifacts.comprehensive_test_results`
📄 `artifacts.enhanced_context_test_results`
📄 `artifacts.generated_commands`
📄 `artifacts.multi_site_test_results`
📄 `artifacts.nlp2cmd_monitoring_log`
📄 `artifacts.results.intelligent_nlp2cmd_results`
📄 `artifacts.results.test_results_no_llm`
📄 `artifacts.results.test_results_with_llm`
📄 `artifacts.sequential_benchmark_results`
📄 `artifacts.web_schema_test_results`
📄 `benchmark_output.benchmark_command_errors`
📄 `benchmark_output.benchmark_results`
📄 `benchmark_output.learning_benchmark`
📄 `benchmark_output.refactoring_plan`
📄 `benchmarks.README`
📄 `benchmarks.learning_benchmark` (6 functions)
📄 `benchmarks.llm_benchmark` (14 functions, 2 classes)
📄 `benchmarks.thermodynamic_benchmark` (7 functions, 1 classes)
📄 `code2llm_workaround`
📄 `command_schemas.browser.click`
📄 `command_schemas.browser.navigate`
📄 `command_schemas.browser.open_url`
📄 `command_schemas.browser.search`
📄 `command_schemas.browser.type_text`
📄 `command_schemas.commands.black`
📄 `command_schemas.commands.cat`
📄 `command_schemas.commands.chmod`
📄 `command_schemas.commands.cp`
📄 `command_schemas.commands.df`
📄 `command_schemas.commands.docker`
📄 `command_schemas.commands.docker.appspec`
📄 `command_schemas.commands.eslint`
📄 `command_schemas.commands.find`
📄 `command_schemas.commands.free`
📄 `command_schemas.commands.git`
📄 `command_schemas.commands.gpg`
📄 `command_schemas.commands.grep`
📄 `command_schemas.commands.iconv`
📄 `command_schemas.commands.iptables`
📄 `command_schemas.commands.jq`
📄 `command_schemas.commands.kubectl`
📄 `command_schemas.commands.kubectl.appspec`
📄 `command_schemas.commands.ls`
📄 `command_schemas.commands.lsof`
📄 `command_schemas.commands.make`
📄 `command_schemas.commands.mongodump`
📄 `command_schemas.commands.mv`
📄 `command_schemas.commands.mysql`
📄 `command_schemas.commands.mysqldump`
📄 `command_schemas.commands.netstat`
📄 `command_schemas.commands.nmap`
📄 `command_schemas.commands.node`
📄 `command_schemas.commands.npm`
📄 `command_schemas.commands.nslookup`
📄 `command_schemas.commands.openssl`
📄 `command_schemas.commands.pip`
📄 `command_schemas.commands.ps`
📄 `command_schemas.commands.psql`
📄 `command_schemas.commands.pytest`
📄 `command_schemas.commands.python3`
📄 `command_schemas.commands.rm`
📄 `command_schemas.commands.rsync`
📄 `command_schemas.commands.sed`
📄 `command_schemas.commands.sensors`
📄 `command_schemas.commands.sort`
📄 `command_schemas.commands.split`
📄 `command_schemas.commands.ssh-keygen`
📄 `command_schemas.commands.tar`
📄 `command_schemas.commands.traceroute`
📄 `command_schemas.commands.uptime`
📄 `command_schemas.commands.zip`
📄 `command_schemas.docker`
📄 `command_schemas.docker.appspec`
📄 `command_schemas.exports.all_schemas`
📄 `command_schemas.exports.batches.batch_1_detailed`
📄 `command_schemas.exports.batches.batch_1_test`
📄 `command_schemas.exports.batches.batch_2_test`
📄 `command_schemas.exports.batches.batch_3_final`
📄 `command_schemas.exports.batches.batch_3_test`
📄 `command_schemas.exports.batches.quick_batch_1_llm`
📄 `command_schemas.exports.batches.quick_batch_2_llm`
📄 `command_schemas.exports.batches.quick_batch_3_llm`
📄 `command_schemas.exports.dynamic.generated_docker_dynamic_schema`
📄 `command_schemas.exports.dynamic.generated_kubectl_dynamic_schema`
📄 `command_schemas.exports.generated_schemas`
📄 `command_schemas.exports.validated_schemas`
📄 `command_schemas.index`
📄 `command_schemas.keyboard.linux_shortcuts`
📄 `command_schemas.keyboard.macos_shortcuts`
📄 `command_schemas.keyboard.windows_shortcuts`
📄 `command_schemas.nginx`
📄 `config`
📄 `config.README`
📄 `config.litellm_config`
📄 `data.domain_weights`
📄 `data.enhanced_domain_patterns`
📄 `data.enhanced_intents`
📄 `data.entities.apps`
📄 `data.entities.colors`
📄 `data.entities.shapes`
📄 `data.form_schema`
📄 `data.intents.close_app`
📄 `data.intents.draw`
📄 `data.intents.email_check`
📄 `data.intents.email_compose`
📄 `data.intents.minimize_all`
📄 `data.intents.navigate`
📄 `data.intents.new_tab`
📄 `data.intents.open_app`
📄 `data.intents.screenshot`
📄 `data.patterns`
📄 `data.phrase_database`
📄 `data.polish_intent_mappings`
📄 `data.polish_shell_patterns`
📄 `data.polish_table_mappings`
📄 `data.prompt`
📄 `data.templates`
📄 `docker-compose`
📄 `docker.novnc.Dockerfile`
📄 `docker.novnc.demos.demo_desktop_gui` (6 functions)
📄 `docker.novnc.docker-compose`
📄 `docker.novnc.start-vnc`
📄 `docs.README`
📄 `docs.SCHEMA_VALIDATION_REPORT`
📄 `docs.api.README`
📄 `docs.architecture.CANVAS_DRAWING`
📄 `docs.architecture.DESKTOP_GUI_AUTOMATION`
📄 `docs.architecture.KEYWORD_DETECTION_FLOW`
📄 `docs.architecture.schema-system`
📄 `docs.architecture.thermodynamic-computing`
📄 `docs.architecture.web-automation`
📄 `docs.development.BENCHMARKING`
📄 `docs.development.FIREFOX_SESSION_INJECTION`
📄 `docs.development.SERVICE_MODE`
📄 `docs.development.STREAM_PROTOCOLS`
📄 `docs.maintainers.IMPROVEMENTS`
📄 `docs.maintainers.PROJECT_HISTORY`
📄 `docs.maintainers.README`
📄 `docs.maintainers.SCHEMA_CONSOLIDATION_SUMMARY`
📄 `docs.maintainers.TEST_SCRIPTS_README`
📄 `docs.maintainers.TODO`
📄 `docs.reference.cli-reference`
📄 `docs.reference.examples-guide`
📄 `docs.reference.python-api`
📄 `docs.user-guide.user-guide`
📄 `examples` (1 functions)
📄 `examples.01_basics.README`
📄 `examples.01_basics.app2schema.README`
📄 `examples.01_basics.app2schema.example` (1 functions)
📄 `examples.01_basics.app2schema.generated_appspec`
📄 `examples.01_basics.docker_basics.01_basics_docker_nlp2cmd` (3 functions)
📄 `examples.01_basics.docker_basics.command_schemas.commands.docker.appspec`
📄 `examples.01_basics.docker_basics.example` (1 functions)
📄 `examples.01_basics.docker_basics.file_repair` (4 functions)
📄 `examples.01_basics.kubernetes_basics.command_schemas.exports.dynamic.kubectl_dynamic_schema`
📄 `examples.01_basics.kubernetes_basics.example` (1 functions)
📄 `examples.01_basics.shell_fundamentals.01_basics_shell_nlp2cmd` (3 functions)
📄 `examples.01_basics.shell_fundamentals.README`
📄 `examples.01_basics.shell_fundamentals.appspec_cache`
📄 `examples.01_basics.shell_fundamentals.environment_analysis` (2 functions)
📄 `examples.01_basics.shell_fundamentals.example` (1 functions)
📄 `examples.01_basics.shell_fundamentals.feedback_loop` (1 functions)
📄 `examples.01_basics.shell_fundamentals.generated_shell_appspec`
📄 `examples.01_basics.shell_fundamentals.generated_shell_dynamic_schema`
📄 `examples.01_basics.shell_fundamentals.runtime_schemas`
📄 `examples.01_basics.shell_fundamentals.schema_cache` (1 functions)
📄 `examples.01_basics.sql_basics.README`
📄 `examples.01_basics.sql_basics.advanced` (1 functions)
📄 `examples.01_basics.sql_basics.example` (1 functions)
📄 `examples.01_basics.sql_basics.llm_integration` (6 functions, 1 classes)
📄 `examples.01_basics.sql_basics.workflows` (2 functions)
📄 `examples.02_benchmarks.README`
📄 `examples.02_benchmarks.performance_testing.README`
📄 `examples.02_benchmarks.performance_testing.benchmark` (9 functions)
📄 `examples.02_benchmarks.performance_testing.benchmark_report`
📄 `examples.02_benchmarks.sequential_testing.benchmark` (3 functions)
📄 `examples.02_benchmarks.sequential_testing.sequential_benchmark_results`
📄 `examples.03_integrations.README`
📄 `examples.03_integrations.pipelines.infrastructure_health` (6 functions)
📄 `examples.03_integrations.pipelines.log_analysis` (4 functions)
📄 `examples.03_integrations.toon_format.01_basic_usage.README`
📄 `examples.03_integrations.toon_format.01_basic_usage.demo` (1 functions)
📄 `examples.03_integrations.toon_format.01_basic_usage.run`
📄 `examples.03_integrations.toon_format.02_command_generator.README`
📄 `examples.03_integrations.toon_format.02_command_generator.demo` (1 functions)
📄 `examples.03_integrations.toon_format.02_command_generator.run`
📄 `examples.03_integrations.toon_format.03_data_manager.README`
📄 `examples.03_integrations.toon_format.03_data_manager.demo` (1 functions)
📄 `examples.03_integrations.toon_format.03_data_manager.run`
📄 `examples.03_integrations.toon_format.04_search_and_filter.README`
📄 `examples.03_integrations.toon_format.04_search_and_filter.demo` (1 functions)
📄 `examples.03_integrations.toon_format.04_search_and_filter.run`
📄 `examples.03_integrations.toon_format.05_advanced_patterns.README`
📄 `examples.03_integrations.toon_format.05_advanced_patterns.demo` (1 functions)
📄 `examples.03_integrations.toon_format.05_advanced_patterns.run`
📄 `examples.03_integrations.toon_format.06_old_system_mock.README`
📄 `examples.03_integrations.toon_format.06_old_system_mock.demo` (4 functions, 1 classes)
📄 `examples.03_integrations.toon_format.06_old_system_mock.run`
📄 `examples.03_integrations.toon_format.07_loading_performance.README`
📄 `examples.03_integrations.toon_format.07_loading_performance.demo` (3 functions)
📄 `examples.03_integrations.toon_format.07_loading_performance.run`
📄 `examples.03_integrations.toon_format.08_memory_usage.README`
📄 `examples.03_integrations.toon_format.08_memory_usage.demo` (4 functions)
📄 `examples.03_integrations.toon_format.08_memory_usage.run`
📄 `examples.03_integrations.toon_format.10_migration_guide.README`
📄 `examples.03_integrations.toon_format.10_migration_guide.run`
📄 `examples.03_integrations.toon_format.11_basic_integration.README`
📄 `examples.03_integrations.toon_format.11_basic_integration.demo` (1 functions)
📄 `examples.03_integrations.toon_format.11_basic_integration.run`
📄 `examples.03_integrations.toon_format.12_advanced_integration.README`
📄 `examples.03_integrations.toon_format.12_advanced_integration.demo` (1 functions)
📄 `examples.03_integrations.toon_format.12_advanced_integration.run`
📄 `examples.03_integrations.toon_format.13_query_system.README`
📄 `examples.03_integrations.toon_format.13_query_system.demo` (1 functions)
📄 `examples.03_integrations.toon_format.13_query_system.run`
📄 `examples.03_integrations.toon_format.14_batch_processing.README`
📄 `examples.03_integrations.toon_format.14_batch_processing.demo` (3 functions)
📄 `examples.03_integrations.toon_format.14_batch_processing.run`
📄 `examples.03_integrations.toon_format.README`
📄 `examples.03_integrations.toon_format.comparison_demo` (16 functions, 2 classes)
📄 `examples.03_integrations.toon_format.practical_usage` (8 functions, 1 classes)
📄 `examples.03_integrations.toon_format.simple_demo` (6 functions)
📄 `examples.03_integrations.toon_format.usage_example` (1 functions)
📄 `examples.03_integrations.validation.config_validation` (3 functions)
📄 `examples.03_integrations.web_development.01_basic_service_config.README`
📄 `examples.03_integrations.web_development.01_basic_service_config.demo` (1 functions, 2 classes)
📄 `examples.03_integrations.web_development.01_basic_service_config.run`
📄 `examples.03_integrations.web_development.02_deployment_planning.README`
📄 `examples.03_integrations.web_development.02_deployment_planning.demo` (2 functions, 2 classes)
📄 `examples.03_integrations.web_development.02_deployment_planning.run`
📄 `examples.03_integrations.web_development.03_docker_compose.README`
📄 `examples.03_integrations.web_development.03_docker_compose.demo` (2 functions, 1 classes)
📄 `examples.03_integrations.web_development.03_docker_compose.run`
📄 `examples.03_integrations.web_development.04_service_deployment.README`
📄 `examples.03_integrations.web_development.04_service_deployment.demo` (1 functions, 1 classes)
📄 `examples.03_integrations.web_development.04_service_deployment.run`
📄 `examples.03_integrations.web_development.05_infrastructure_management.README`
📄 `examples.03_integrations.web_development.05_infrastructure_management.demo` (1 functions, 1 classes)
📄 `examples.03_integrations.web_development.05_infrastructure_management.run`
📄 `examples.03_integrations.web_development.README`
📄 `examples.03_integrations.web_development.README_WEB_BACKEND`
📄 `examples.03_integrations.web_development.demo` (3 functions)
📄 `examples.03_integrations.web_development.demo_auto` (6 functions)
📄 `examples.03_integrations.web_development.demo_batch` (5 functions)
📄 `examples.03_integrations.web_development.nlp2cmd_web_controller` (52 functions, 8 classes)
📄 `examples.03_integrations.web_development.prompt`
📄 `examples.03_integrations.web_development.web_app_example` (8 functions, 3 classes)
📄 `examples.03_integrations.web_development.web_generated.chat-service-config`
📄 `examples.03_integrations.web_development.web_generated.chat-service-docker-compose`
📦 `examples.04_domain_specific`
📄 `examples.04_domain_specific.README`
📄 `examples.04_domain_specific.SUMMARY`
📄 `examples.04_domain_specific._demo_helpers` (12 functions)
📄 `examples.04_domain_specific.api_key_prompts` (2 functions, 1 classes)
📄 `examples.04_domain_specific.bioinformatics.01_sequence_analysis.README`
📄 `examples.04_domain_specific.bioinformatics.01_sequence_analysis.demo` (1 functions, 1 classes)
📄 `examples.04_domain_specific.bioinformatics.01_sequence_analysis.run`
📄 `examples.04_domain_specific.bioinformatics.02_file_processing.README`
📄 `examples.04_domain_specific.bioinformatics.02_file_processing.demo` (1 functions, 1 classes)
📄 `examples.04_domain_specific.bioinformatics.02_file_processing.run`
📄 `examples.04_domain_specific.bioinformatics.03_blast_operations.README`
📄 `examples.04_domain_specific.bioinformatics.03_blast_operations.demo` (1 functions, 1 classes)
📄 `examples.04_domain_specific.bioinformatics.03_blast_operations.run`
📄 `examples.04_domain_specific.bioinformatics.04_data_conversion.README`
📄 `examples.04_domain_specific.bioinformatics.04_data_conversion.demo` (1 functions, 1 classes)
📄 `examples.04_domain_specific.bioinformatics.04_data_conversion.run`
📄 `examples.04_domain_specific.bioinformatics.05_pipeline_automation.README`
📄 `examples.04_domain_specific.bioinformatics.05_pipeline_automation.demo` (1 functions, 1 classes)
📄 `examples.04_domain_specific.bioinformatics.05_pipeline_automation.run`
📄 `examples.04_domain_specific.bioinformatics.README`
📄 `examples.04_domain_specific.bioinformatics.complete_examples` (7 functions)
📄 `examples.04_domain_specific.bioinformatics.example` (6 functions)
📄 `examples.04_domain_specific.data_science.dsl_demo` (11 functions)
📄 `examples.04_domain_specific.data_science.example` (5 functions)
📄 `examples.04_domain_specific.debugging.01_python_api_concept.README`
📄 `examples.04_domain_specific.debugging.01_python_api_concept.demo` (1 functions)
📄 `examples.04_domain_specific.debugging.01_python_api_concept.run`
📄 `examples.04_domain_specific.debugging.02_shell_commands.README`
📄 `examples.04_domain_specific.debugging.02_shell_commands.demo` (1 functions)
📄 `examples.04_domain_specific.debugging.02_shell_commands.run`
📄 `examples.04_domain_specific.debugging.03_mixed_workflow.README`
📄 `examples.04_domain_specific.debugging.03_mixed_workflow.demo` (1 functions)
📄 `examples.04_domain_specific.debugging.03_mixed_workflow.run`
📄 `examples.04_domain_specific.debugging.04_advanced_patterns.README`
📄 `examples.04_domain_specific.debugging.04_advanced_patterns.demo` (1 functions)
📄 `examples.04_domain_specific.debugging.04_advanced_patterns.run`
📄 `examples.04_domain_specific.debugging.05_real_world_examples.README`
📄 `examples.04_domain_specific.debugging.05_real_world_examples.demo` (1 functions)
📄 `examples.04_domain_specific.debugging.05_real_world_examples.run`
📄 `examples.04_domain_specific.debugging.06_test_framework.README`
📄 `examples.04_domain_specific.debugging.06_test_framework.demo` (4 functions, 2 classes)
📄 `examples.04_domain_specific.debugging.06_test_framework.run`
📄 `examples.04_domain_specific.debugging.07_file_operations.README`
📄 `examples.04_domain_specific.debugging.07_file_operations.demo` (1 functions, 1 classes)
📄 `examples.04_domain_specific.debugging.07_file_operations.run`
📄 `examples.04_domain_specific.debugging.08_system_commands.README`
📄 `examples.04_domain_specific.debugging.08_system_commands.demo` (1 functions, 1 classes)
📄 `examples.04_domain_specific.debugging.08_system_commands.run`
📄 `examples.04_domain_specific.debugging.09_network_commands.README`
📄 `examples.04_domain_specific.debugging.09_network_commands.demo` (1 functions, 1 classes)
📄 `examples.04_domain_specific.debugging.09_network_commands.run`
📄 `examples.04_domain_specific.debugging.10_advanced_validation.README`
📄 `examples.04_domain_specific.debugging.10_advanced_validation.demo` (5 functions, 2 classes)
📄 `examples.04_domain_specific.debugging.10_advanced_validation.run`
📄 `examples.04_domain_specific.debugging.README`
📄 `examples.04_domain_specific.debugging.commands_demo`
📄 `examples.04_domain_specific.debugging.generator` (1 functions)
📄 `examples.04_domain_specific.debugging.intents` (1 functions)
📄 `examples.04_domain_specific.debugging.keywords` (1 functions)
📄 `examples.04_domain_specific.debugging.simple_demo` (7 functions)
📄 `examples.04_domain_specific.debugging.validation` (7 functions, 2 classes)
📄 `examples.04_domain_specific.debugging.validation_report`
📄 `examples.04_domain_specific.devops.example` (4 functions)
📄 `examples.04_domain_specific.drug_discovery.example` (3 functions)
📄 `examples.04_domain_specific.education.example` (8 functions)
📄 `examples.04_domain_specific.energy.example` (8 functions)
📄 `examples.04_domain_specific.finance.example` (7 functions)
📄 `examples.04_domain_specific.healthcare.example` (8 functions)
📄 `examples.04_domain_specific.logistics.example` (7 functions)
📄 `examples.04_domain_specific.physics.example` (8 functions)
📄 `examples.04_domain_specific.polish_llm_integration.01_pdf_extraction.README`
📄 `examples.04_domain_specific.polish_llm_integration.01_pdf_extraction.demo` (5 functions, 1 classes)
📄 `examples.04_domain_specific.polish_llm_integration.01_pdf_extraction.run`
📄 `examples.04_domain_specific.polish_llm_integration.02_text_chunking.README`
📄 `examples.04_domain_specific.polish_llm_integration.02_text_chunking.demo` (4 functions, 1 classes)
📄 `examples.04_domain_specific.polish_llm_integration.02_text_chunking.run`
📄 `examples.04_domain_specific.polish_llm_integration.03_llm_search.README`
📄 `examples.04_domain_specific.polish_llm_integration.03_llm_search.demo` (5 functions, 1 classes)
📄 `examples.04_domain_specific.polish_llm_integration.03_llm_search.run`
📄 `examples.04_domain_specific.polish_llm_integration.04_results_ranking.README`
📄 `examples.04_domain_specific.polish_llm_integration.04_results_ranking.demo` (5 functions, 2 classes)
📄 `examples.04_domain_specific.polish_llm_integration.04_results_ranking.run`
📄 `examples.04_domain_specific.polish_llm_integration.05_integration.README`
📄 `examples.04_domain_specific.polish_llm_integration.05_integration.demo` (8 functions, 4 classes)
📄 `examples.04_domain_specific.polish_llm_integration.05_integration.run`
📄 `examples.04_domain_specific.polish_llm_integration.README`
📄 `examples.04_domain_specific.polish_llm_integration.download_bielik` (1 functions)
📄 `examples.04_domain_specific.polish_llm_integration.example_pdf_search` (9 functions, 2 classes)
📄 `examples.04_domain_specific.polish_llm_integration.mock_test_polish_llm` (7 functions, 2 classes)
📄 `examples.04_domain_specific.polish_llm_integration.setup_and_test_bielik` (8 functions, 1 classes)
📄 `examples.04_domain_specific.run_all` (2 functions)
📄 `examples.04_domain_specific.smart_cities.example` (8 functions)
📄 `examples.05_advanced_features.README`
📄 `examples.05_advanced_features.dynamic_schemas.README`
📄 `examples.05_advanced_features.dynamic_schemas.demo_enhanced` (1 functions)
📄 `examples.05_advanced_features.dynamic_schemas.demo_intelligent_nlp2cmd` (9 functions, 1 classes)
📄 `examples.05_advanced_features.dynamic_schemas.demo_persistent_storage` (2 functions)
📄 `examples.05_advanced_features.dynamic_schemas.demo_schema_flow` (4 functions)
📄 `examples.05_advanced_features.dynamic_schemas.demo_version_detection` (4 functions)
📄 `examples.05_advanced_features.dynamic_schemas.example` (1 functions)
📄 `examples.05_advanced_features.dynamic_schemas.schema_flow_demo` (4 functions)
📄 `examples.05_advanced_features.dynamic_schemas.simple_schema_demo` (1 functions)
📄 `examples.05_advanced_features.schema_driven_architecture.01_architecture_overview.run`
📄 `examples.05_advanced_features.schema_driven_architecture.02_decision_router.README`
📄 `examples.05_advanced_features.schema_driven_architecture.02_decision_router.demo` (3 functions, 2 classes)
📄 `examples.05_advanced_features.schema_driven_architecture.02_decision_router.run`
📄 `examples.05_advanced_features.schema_driven_architecture.03_llm_planner.README`
📄 `examples.05_advanced_features.schema_driven_architecture.03_llm_planner.demo` (2 functions, 2 classes)
📄 `examples.05_advanced_features.schema_driven_architecture.03_llm_planner.run`
📄 `examples.05_advanced_features.schema_driven_architecture.04_plan_executor.README`
📄 `examples.05_advanced_features.schema_driven_architecture.04_plan_executor.demo` (9 functions, 2 classes)
📄 `examples.05_advanced_features.schema_driven_architecture.05_result_aggregator.README`
📄 `examples.05_advanced_features.schema_driven_architecture.05_result_aggregator.demo` (6 functions, 3 classes)
📄 `examples.05_advanced_features.schema_driven_architecture.05_result_aggregator.run`
📄 `examples.05_advanced_features.schema_driven_architecture.end_to_end_demo` (7 functions)
📄 `examples.05_advanced_features.schema_driven_architecture.manual_appspec` (1 functions)
📄 `examples.05_advanced_features.schema_driven_architecture.mvp` (1 functions)
📄 `examples.05_advanced_features.thermodynamic_computing.README`
📄 `examples.05_advanced_features.thermodynamic_computing.example` (7 functions)
📄 `examples.06_desktop_automation.00_full_lifecycle.README`
📄 `examples.06_desktop_automation.00_full_lifecycle.run` (1 functions)
📄 `examples.06_desktop_automation.01_terminal.README`
📄 `examples.06_desktop_automation.01_terminal.logs.session`
📄 `examples.06_desktop_automation.01_terminal.run`
📄 `examples.06_desktop_automation.02_calculator.README`
📄 `examples.06_desktop_automation.02_calculator.run`
📄 `examples.06_desktop_automation.03_text_editor.README`
📄 `examples.06_desktop_automation.03_text_editor.run`
📄 `examples.06_desktop_automation.04_browser_tabs.README`
📄 `examples.06_desktop_automation.04_browser_tabs.run`
📄 `examples.06_desktop_automation.05_email_client.README`
📄 `examples.06_desktop_automation.05_email_client.run`
📄 `examples.06_desktop_automation.06_env_extract.README`
📄 `examples.06_desktop_automation.06_env_extract.run` (1 functions)
📄 `examples.06_desktop_automation.07_canvas_drawing.README`
📄 `examples.06_desktop_automation.07_canvas_drawing.run` (1 functions)
📄 `examples.06_desktop_automation.08_captcha_solver.README`
📄 `examples.06_desktop_automation.08_captcha_solver.run` (1 functions)
📄 `examples.06_desktop_automation.09_complex_commands.README`
📄 `examples.06_desktop_automation.09_complex_commands.run` (1 functions)
📄 `examples.06_desktop_automation.README`
📄 `examples.06_desktop_automation.calculator_session`
📄 `examples.06_desktop_automation.multi_app_session`
📄 `examples.06_desktop_automation.terminal_session`
📄 `examples.06_tools_and_utilities.README`
📄 `examples.06_tools_and_utilities.migration_tools.README`
📄 `examples.06_tools_and_utilities.migration_tools.demo_versioned_schemas` (4 functions)
📄 `examples.06_tools_and_utilities.migration_tools.guide` (6 functions)
📄 `examples.07_browser_automation.01_screenshot_only`
📄 `examples.07_browser_automation.02_video_only`
📄 `examples.07_browser_automation.03_interactive_mode`
📄 `examples.07_browser_automation.04_oferteo_extraction`
📄 `examples.07_browser_automation.05_simple_formfill`
📄 `examples.07_browser_automation.06_formfill_with_discovery`
📄 `examples.07_browser_automation.07_batch_multiple`
📄 `examples.07_browser_automation.README`
📄 `examples.07_stream_protocols.README`
📄 `examples.07_stream_protocols.example_http_api` (1 functions)
📄 `examples.07_stream_protocols.example_libvirt` (1 functions)
📄 `examples.07_stream_protocols.example_multi_stream` (1 functions)
📄 `examples.07_stream_protocols.example_rtsp` (1 functions)
📄 `examples.07_stream_protocols.example_ssh` (1 functions)
📄 `examples.08_api_key_management.01_diagnose_credentials.run` (1 functions)
📄 `examples.08_api_key_management.01_diagnose_credentials_nlp2cmd` (3 functions)
📄 `examples.08_api_key_management.02_openrouter_key.run` (3 functions)
📄 `examples.08_api_key_management.03_github_token.run` (3 functions)
📄 `examples.08_api_key_management.04_huggingface_token.run` (3 functions)
📄 `examples.08_api_key_management.05_openai_key.run` (3 functions)
📄 `examples.08_api_key_management.06_multi_provider.run` (5 functions)
📄 `examples.08_api_key_management.README`
📄 `examples.08_llm_validation.README`
📄 `examples.08_llm_validation.benchmark_after`
📄 `examples.08_llm_validation.benchmark_before`
📄 `examples.08_llm_validation.benchmark_validator` (3 functions, 2 classes)
📄 `examples.08_llm_validation.demo_validation`
📄 `examples.08_llm_validation.test_feedback_results`
📄 `examples.08_llm_validation.test_results`
📄 `examples.09_online_drawing.01_draw_chat.README`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_142425`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_142636`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_142823`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_143953`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_144325`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_144543`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_170506`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_170729`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_170742`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_170840`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_171110`
📄 `examples.09_online_drawing.01_draw_chat.logs.01_draw_chat_20260303_171804`
📄 `examples.09_online_drawing.01_draw_chat.run` (1 functions)
📄 `examples.09_online_drawing.02_picsart.README`
📄 `examples.09_online_drawing.02_picsart.logs.02_picsart_20260303_142942`
📄 `examples.09_online_drawing.02_picsart.logs.02_picsart_20260303_144722`
📄 `examples.09_online_drawing.02_picsart.logs.02_picsart_20260303_144922`
📄 `examples.09_online_drawing.02_picsart.logs.02_picsart_20260303_171011`
📄 `examples.09_online_drawing.02_picsart.run` (1 functions)
📄 `examples.09_online_drawing.03_adaptive.README`
📄 `examples.09_online_drawing.03_adaptive.logs.03_adaptive_20260303_143144`
📄 `examples.09_online_drawing.03_adaptive.logs.03_adaptive_20260303_145059`
📄 `examples.09_online_drawing.03_adaptive.logs.03_adaptive_20260303_145342`
📄 `examples.09_online_drawing.03_adaptive.logs.03_adaptive_20260303_170902`
📄 `examples.09_online_drawing.03_adaptive.logs.03_adaptive_20260303_170926`
📄 `examples.09_online_drawing.03_adaptive.logs.03_adaptive_20260303_171825`
📄 `examples.09_online_drawing.03_adaptive.run` (1 functions)
📄 `examples.09_online_drawing.04_object_database.README`
📄 `examples.09_online_drawing.04_object_database.run` (4 functions)
📄 `examples.09_online_drawing.05_autonomous.README`
📄 `examples.09_online_drawing.05_autonomous.run` (3 functions)
📄 `examples.09_online_drawing.06_visual_validator.README`
📄 `examples.09_online_drawing.06_visual_validator.logs.validation_star_red`
📄 `examples.09_online_drawing.06_visual_validator.run` (4 functions)
📄 `examples.09_online_drawing.07_shape_gallery.README`
📄 `examples.09_online_drawing.07_shape_gallery.run` (8 functions)
📄 `examples.09_online_drawing.08_search_demo.README`
📄 `examples.09_online_drawing.08_search_demo.run` (2 functions)
📄 `examples.09_online_drawing.09_evolutionary_orchestrator.README`
📄 `examples.09_online_drawing.09_evolutionary_orchestrator.run` (5 functions)
📄 `examples.09_online_drawing.ANALYSIS`
📄 `examples.09_online_drawing.CHANGELOG`
📄 `examples.09_online_drawing.README`
📄 `examples.09_online_drawing._old.01_draw_chat_shapes` (1 functions)
📄 `examples.09_online_drawing._old.01_draw_chat_shapes_nlp2cmd` (4 functions)
📄 `examples.09_online_drawing._old.02_picsart_painting` (1 functions)
📄 `examples.09_online_drawing._old.02_picsart_painting_nlp2cmd` (4 functions)
📄 `examples.09_online_drawing._old.03_adaptive_drawing` (2 functions)
📄 `examples.09_online_drawing._old.03_adaptive_drawing_nlp2cmd` (4 functions)
📄 `examples.09_online_drawing._old.04_object_database_drawing` (15 functions, 3 classes)
📄 `examples.09_online_drawing._old.05_autonomous_drawing` (4 functions)
📄 `examples.09_online_drawing._run_utils` (22 functions, 2 classes)
📄 `examples.09_online_drawing.run` (4 functions)
📄 `examples.10_online_code_editors.01_codepen_live` (4 functions)
📄 `examples.10_online_code_editors.01_codepen_live_nlp2cmd` (3 functions)
📄 `examples.10_online_code_editors.02_mycompiler_run` (1 functions)
📄 `examples.10_online_code_editors.02_mycompiler_run_nlp2cmd` (3 functions)
📄 `examples.10_online_code_editors.03_adaptive_code` (4 functions)
📄 `examples.10_online_code_editors.03_adaptive_code_nlp2cmd` (2 functions)
📄 `examples.10_online_code_editors.04_jsfiddle_frontend` (1 functions)
📄 `examples.10_online_code_editors.04_jsfiddle_frontend_nlp2cmd` (3 functions)
📄 `examples.10_online_code_editors.05_dynamic_executor` (2 functions)
📄 `examples.10_online_code_editors.05_dynamic_executor_nlp2cmd` (2 functions)
📄 `examples.10_online_code_editors.README`
📄 `examples.MAKEFILE_PROSTY`
📄 `examples.Makefile`
📄 `examples.README`
📄 `examples.README_NLP2CMD`
📄 `examples._dynamic_orchestrator` (2 functions, 1 classes)
📄 `examples._example_helpers` (2 functions)
📄 `examples._verbose_helper` (9 functions)
📄 `examples.demo_screenshot_video`
📄 `examples.run_examples` (10 functions)
📄 `examples.run_task` (1 functions)
📄 `examples.show_metrics` (1 functions)
📄 `generate_chunks`
📄 `generate_quick`
📄 `generate_working`
📄 `generated_appspec`
📄 `goal`
📄 `install_vnc`
📄 `jspaint_app_test4` (1 functions)
📄 `manual_appspec`
📄 `oferteo_pl_data`
📄 `out_call_graph`
📄 `out_function_entries`
📄 `out_interprocedural_decision_paths`
📄 `planfile`
📄 `prefact`
📄 `project`
📄 `projektor`
📄 `pyproject`
📄 `pyqual`
📄 `pytest`
📄 `requirements`
📄 `requirements-enhanced`
📄 `requirements-minimal`
📄 `requirements-thermodynamic`
📄 `requirements.llm`
📄 `run_all_tests`
📄 `run_test`
📄 `scripts.bump_version` (1 functions)
📄 `scripts.install_desktop_tools` (5 functions)
📄 `scripts.maintenance.apply_complexity_refactors` (1 functions)
📄 `scripts.maintenance.apply_nlp2cmd_fixes` (5 functions)
📄 `scripts.maintenance.apply_polish_integration` (4 functions)
📄 `scripts.maintenance.apply_refactors_to_source` (4 functions)
📄 `scripts.maintenance.auto_apply_refactors` (3 functions)
📄 `scripts.maintenance.cyclomatic_complexity_refactor_report`
📄 `scripts.maintenance.final_analysis_and_next_steps` (10 functions, 1 classes)
📄 `scripts.maintenance.final_project_summary` (10 functions, 1 classes)
📄 `scripts.maintenance.fix_comprehensive_test_issues` (9 functions, 1 classes)
📄 `scripts.maintenance.generate_refactor_report` (1 functions)
📄 `scripts.maintenance.implement_core_integration` (10 functions, 1 classes)
📄 `scripts.maintenance.implement_high_priority_fixes` (10 functions, 1 classes)
📄 `scripts.maintenance.llx_refactor` (6 functions)
📄 `scripts.maintenance.refactor_detect_normalized` (10 functions)
📄 `scripts.maintenance.refactor_shell_entities` (11 functions)
📄 `scripts.maintenance.refactoring_summary` (1 functions)
📄 `scripts.maintenance.restore_system` (4 functions)
📄 `scripts.maintenance.split_pipeline_runner` (2 functions)
📄 `scripts.setup_external` (1 functions)
📄 `scripts.test_commands_docker`
📄 `scripts.testing.compare_entity_extractors` (7 functions)
📄 `scripts.testing.run_e2e_tests` (16 functions, 1 classes)
📄 `scripts.thermodynamic.termo` (4 functions)
📄 `scripts.thermodynamic.termo1` (1 functions)
📄 `scripts.thermodynamic.termo2` (38 functions, 12 classes)
📄 `scripts.thermodynamic.termo_demo` (5 functions)
📦 `src.app2schema`
📄 `src.app2schema.__main__`
📄 `src.app2schema.cli` (1 functions)
📄 `src.app2schema.extract` (15 functions, 2 classes)
📦 `src.nlp2cmd`
📄 `src.nlp2cmd.__main__`
📦 `src.nlp2cmd.adapters`
📄 `src.nlp2cmd.adapters.appspec` (6 functions, 2 classes)
📄 `src.nlp2cmd.adapters.base` (12 functions, 3 classes)
📄 `src.nlp2cmd.adapters.browser` (26 functions, 2 classes)
📄 `src.nlp2cmd.adapters.canvas` (12 functions, 4 classes)
📄 `src.nlp2cmd.adapters.desktop` (21 functions, 3 classes)
📄 `src.nlp2cmd.adapters.docker` (19 functions, 3 classes)
📄 `src.nlp2cmd.adapters.dql` (13 functions, 3 classes)
📄 `src.nlp2cmd.adapters.dynamic` (21 functions, 2 classes)
📄 `src.nlp2cmd.adapters.kubernetes` (23 functions, 3 classes)
📄 `src.nlp2cmd.adapters.shell` (13 functions, 3 classes)
📄 `src.nlp2cmd.adapters.shell_generators` (11 functions, 8 classes)
📄 `src.nlp2cmd.adapters.sql` (15 functions, 3 classes)
📦 `src.nlp2cmd.aggregator` (11 functions, 3 classes)
📄 `src.nlp2cmd.appspec_runtime` (2 functions, 2 classes)
📦 `src.nlp2cmd.automation`
📄 `src.nlp2cmd.automation.action_planner` (27 functions, 3 classes)
📄 `src.nlp2cmd.automation.captcha_solver` (10 functions, 2 classes)
📄 `src.nlp2cmd.automation.complex_planner` (10 functions, 3 classes)
📄 `src.nlp2cmd.automation.drawing_blueprints` (18 functions, 1 classes)
📄 `src.nlp2cmd.automation.env_extractor` (11 functions, 2 classes)
📄 `src.nlp2cmd.automation.feedback_loop` (9 functions, 6 classes)
📄 `src.nlp2cmd.automation.firefox_sessions` (11 functions, 1 classes)
📄 `src.nlp2cmd.automation.mouse_controller` (23 functions, 2 classes)
📄 `src.nlp2cmd.automation.password_store` (24 functions, 6 classes)
📄 `src.nlp2cmd.automation.schema_fallback` (17 functions, 3 classes)
📄 `src.nlp2cmd.automation.service_configs` (2 functions)
📄 `src.nlp2cmd.automation.shape_planner` (5 functions, 1 classes)
📄 `src.nlp2cmd.automation.step_validator` (18 functions, 3 classes)
📄 `src.nlp2cmd.automation.vector_store` (15 functions, 2 classes)
📦 `src.nlp2cmd.browser_manager`
📄 `src.nlp2cmd.browser_manager.base` (1 functions, 3 classes)
📄 `src.nlp2cmd.browser_manager.browser_connector` (4 functions, 1 classes)
📄 `src.nlp2cmd.browser_manager.cdp_detector` (4 functions, 1 classes)
📄 `src.nlp2cmd.browser_manager.existing_browser_manager` (3 functions, 1 classes)
📄 `src.nlp2cmd.browser_manager.token_navigator` (3 functions, 2 classes)
📦 `src.nlp2cmd.browser_token`
📄 `src.nlp2cmd.browser_token.base` (2 classes)
📄 `src.nlp2cmd.browser_token.browser_launcher` (4 functions, 1 classes)
📄 `src.nlp2cmd.browser_token.hf_token_retriever` (2 functions, 1 classes)
📄 `src.nlp2cmd.browser_token.token_navigator` (4 functions, 2 classes)
📄 `src.nlp2cmd.browser_token.token_prompt_handler` (5 functions, 1 classes)
📦 `src.nlp2cmd.canvas_planner`
📄 `src.nlp2cmd.canvas_planner.base` (6 functions, 2 classes)
📄 `src.nlp2cmd.canvas_planner.blueprint_planner` (2 functions, 1 classes)
📄 `src.nlp2cmd.canvas_planner.llm_planner` (4 functions, 1 classes)
📄 `src.nlp2cmd.canvas_planner.orchestrator` (7 functions, 1 classes)
📄 `src.nlp2cmd.canvas_planner.rule_planner` (8 functions, 1 classes)
📄 `src.nlp2cmd.canvas_planner.vector_planner` (6 functions, 1 classes)
📦 `src.nlp2cmd.cli`
📄 `src.nlp2cmd.cli.auto_repair` (12 functions, 3 classes)
📄 `src.nlp2cmd.cli.cache` (9 functions)
📦 `src.nlp2cmd.cli.commands`
📄 `src.nlp2cmd.cli.commands.doctor` (23 functions, 3 classes)
📄 `src.nlp2cmd.cli.commands.examples` (13 functions, 3 classes)
📄 `src.nlp2cmd.cli.commands.generate` (4 functions)
📄 `src.nlp2cmd.cli.commands.interactive` (9 functions, 1 classes)
📄 `src.nlp2cmd.cli.commands.run` (4 functions)
📄 `src.nlp2cmd.cli.commands.tools` (3 functions)
📄 `src.nlp2cmd.cli.debug_info` (3 functions)
📄 `src.nlp2cmd.cli.display` (12 functions)
📄 `src.nlp2cmd.cli.helpers` (10 functions)
📄 `src.nlp2cmd.cli.history` (6 functions)
📄 `src.nlp2cmd.cli.main` (13 functions)
📄 `src.nlp2cmd.cli.markdown_output` (14 functions, 2 classes)
📄 `src.nlp2cmd.cli.session_logger` (12 functions, 1 classes)
📄 `src.nlp2cmd.cli.syntax_cache` (8 functions, 1 classes)
📄 `src.nlp2cmd.cli.web_schema` (5 functions)
📦 `src.nlp2cmd.context`
📄 `src.nlp2cmd.context.disambiguator` (5 functions, 2 classes)
📦 `src.nlp2cmd.core`
📄 `src.nlp2cmd.core.core_backends` (12 functions, 4 classes)
📄 `src.nlp2cmd.core.core_models` (12 functions, 5 classes)
📄 `src.nlp2cmd.core.core_transform` (22 functions, 1 classes)
📄 `src.nlp2cmd.core.toon_integration` (32 functions, 1 classes)
📄 `src.nlp2cmd.data.browser_config.contact_paths`
📄 `src.nlp2cmd.data.browser_config.junk_field_patterns`
📄 `src.nlp2cmd.data.browser_config.selectors`
📄 `src.nlp2cmd.data.command_detector`
📄 `src.nlp2cmd.data.config.intents`
📄 `src.nlp2cmd.data.config.services`
📄 `src.nlp2cmd.data.defaults`
📄 `src.nlp2cmd.data.expanded_phrases`
📄 `src.nlp2cmd.data.form_data`
📄 `src.nlp2cmd.data.form_schema`
📄 `src.nlp2cmd.data.keyword_intent_detector_config`
📄 `src.nlp2cmd.data.multilingual_phrases`
📄 `src.nlp2cmd.data.optimization_schema`
📄 `src.nlp2cmd.data.patterns`
📄 `src.nlp2cmd.data.phrase_database`
📄 `src.nlp2cmd.data.router_config`
📄 `src.nlp2cmd.data.semantic_embeddings`
📄 `src.nlp2cmd.data.shell_execution_policy`
📄 `src.nlp2cmd.data.templates`
📦 `src.nlp2cmd.desktop_executor`
📄 `src.nlp2cmd.desktop_executor.backend_detector` (6 functions, 1 classes)
📄 `src.nlp2cmd.desktop_executor.base` (3 functions, 4 classes)
📄 `src.nlp2cmd.desktop_executor.browser_controller` (5 functions, 1 classes)
📄 `src.nlp2cmd.desktop_executor.desktop_action_executor` (13 functions, 1 classes)
📄 `src.nlp2cmd.desktop_executor.env_manager` (4 functions, 1 classes)
📄 `src.nlp2cmd.desktop_executor.keyboard_controller` (11 functions, 1 classes)
📄 `src.nlp2cmd.desktop_executor.window_manager` (5 functions, 1 classes)
📦 `src.nlp2cmd.dom_actions`
📄 `src.nlp2cmd.dom_actions.base` (3 functions, 3 classes)
📄 `src.nlp2cmd.dom_actions.companies` (8 functions, 1 classes)
📄 `src.nlp2cmd.dom_actions.dispatcher` (4 functions, 1 classes)
📄 `src.nlp2cmd.dom_actions.forms` (8 functions, 1 classes)
📄 `src.nlp2cmd.dom_actions.navigation` (3 functions, 3 classes)
📄 `src.nlp2cmd.dom_actions.registry` (7 functions, 1 classes)
📄 `src.nlp2cmd.dom_actions.save` (6 functions, 2 classes)
📦 `src.nlp2cmd.enhanced` (11 functions, 1 classes)
📦 `src.nlp2cmd.environment` (15 functions, 4 classes)
📦 `src.nlp2cmd.evolutionary`
📄 `src.nlp2cmd.evolutionary.engine` (4 functions, 1 classes)
📄 `src.nlp2cmd.evolutionary.planner` (17 functions, 1 classes)
📄 `src.nlp2cmd.evolutionary.runner` (4 functions, 1 classes)
📄 `src.nlp2cmd.evolutionary.store` (7 functions, 1 classes)
📄 `src.nlp2cmd.evolutionary.types` (3 classes)
📄 `src.nlp2cmd.evolutionary_orchestrator`
📦 `src.nlp2cmd.execution`
📄 `src.nlp2cmd.execution.base` (2 functions, 3 classes)
📄 `src.nlp2cmd.execution.browser` (15 functions, 2 classes)
📄 `src.nlp2cmd.execution.executor_registry` (7 functions, 1 classes)
📄 `src.nlp2cmd.execution.media_recorder` (7 functions, 1 classes)
📄 `src.nlp2cmd.execution.runner` (10 functions, 3 classes)
📄 `src.nlp2cmd.execution.shell_executor` (6 functions, 1 classes)
📦 `src.nlp2cmd.executor` (18 functions, 8 classes)
📦 `src.nlp2cmd.exploration`
📄 `src.nlp2cmd.exploration.base` (12 functions, 4 classes)
📄 `src.nlp2cmd.exploration.data_tree` (12 functions, 3 classes)
📄 `src.nlp2cmd.exploration.disk` (14 functions, 2 classes)
📄 `src.nlp2cmd.exploration.resource_discovery` (10 functions, 3 classes)
📄 `src.nlp2cmd.exploration.service` (11 functions, 3 classes)
📦 `src.nlp2cmd.feedback` (19 functions, 5 classes)
📦 `src.nlp2cmd.generation` (2 functions)
📄 `src.nlp2cmd.generation.auto_repair` (12 functions, 1 classes)
📄 `src.nlp2cmd.generation.complex_detector` (1 functions, 2 classes)
📄 `src.nlp2cmd.generation.data_loader` (28 functions, 3 classes)
📄 `src.nlp2cmd.generation.enhanced_context` (14 functions, 2 classes)
📄 `src.nlp2cmd.generation.evolutionary_cache` (24 functions, 3 classes)
📄 `src.nlp2cmd.generation.fuzzy_schema_matcher` (23 functions, 4 classes)
📄 `src.nlp2cmd.generation.hybrid` (12 functions, 4 classes)
📦 `src.nlp2cmd.generation.keywords`
📄 `src.nlp2cmd.generation.keywords.keyword_detector` (21 functions, 2 classes)
📄 `src.nlp2cmd.generation.keywords.keyword_patterns` (15 functions, 1 classes)
📄 `src.nlp2cmd.generation.llm_multi` (10 functions, 5 classes)
📄 `src.nlp2cmd.generation.llm_simple` (19 functions, 10 classes)
📄 `src.nlp2cmd.generation.ml_intent_classifier` (14 functions, 3 classes)
📄 `src.nlp2cmd.generation.multi_command` (8 functions, 2 classes)
📄 `src.nlp2cmd.generation.pipeline` (15 functions, 1 classes)
📄 `src.nlp2cmd.generation.pipeline_components` (10 functions, 3 classes)
📄 `src.nlp2cmd.generation.regex` (12 functions, 3 classes)
📦 `src.nlp2cmd.generation.schema`
📄 `src.nlp2cmd.generation.schema.adapter` (10 functions, 1 classes)
📄 `src.nlp2cmd.generation.schema.generator` (15 functions, 2 classes)
📄 `src.nlp2cmd.generation.semantic_entities` (7 functions, 1 classes)
📄 `src.nlp2cmd.generation.semantic_matcher_optimized` (30 functions, 3 classes)
📄 `src.nlp2cmd.generation.structured` (7 functions, 5 classes)
📄 `src.nlp2cmd.generation.template_generator` (100 functions, 2 classes)
📦 `src.nlp2cmd.generation.templates`
📄 `src.nlp2cmd.generation.templates.api_templates`
📄 `src.nlp2cmd.generation.templates.browser_templates`
📄 `src.nlp2cmd.generation.templates.data_templates`
📄 `src.nlp2cmd.generation.templates.desktop_templates`
📄 `src.nlp2cmd.generation.templates.devops_templates`
📄 `src.nlp2cmd.generation.templates.docker_templates`
📄 `src.nlp2cmd.generation.templates.ffmpeg_templates`
📄 `src.nlp2cmd.generation.templates.git_templates`
📄 `src.nlp2cmd.generation.templates.iot_templates`
📄 `src.nlp2cmd.generation.templates.kubernetes_templates`
📄 `src.nlp2cmd.generation.templates.media_templates`
📄 `src.nlp2cmd.generation.templates.package_mgmt_templates`
📄 `src.nlp2cmd.generation.templates.presentation_templates`
📄 `src.nlp2cmd.generation.templates.rag_templates`
📄 `src.nlp2cmd.generation.templates.remote_templates`
📄 `src.nlp2cmd.generation.templates.shell_templates`
📄 `src.nlp2cmd.generation.templates.sql_templates`
📄 `src.nlp2cmd.generation.thermodynamic` (14 functions, 5 classes)
📄 `src.nlp2cmd.generation.thermodynamic_components` (11 functions, 4 classes)
📄 `src.nlp2cmd.generation.train_model` (7 functions)
📄 `src.nlp2cmd.generation.validating` (9 functions, 8 classes)
📦 `src.nlp2cmd.history`
📄 `src.nlp2cmd.history.tracker` (18 functions, 3 classes)
📄 `src.nlp2cmd.intelligent.command_detector` (5 functions, 2 classes)
📄 `src.nlp2cmd.intelligent.dynamic_generator` (6 functions, 1 classes)
📄 `src.nlp2cmd.intelligent.version_aware_generator` (11 functions, 1 classes)
📄 `src.nlp2cmd.ir` (1 functions, 1 classes)
📦 `src.nlp2cmd.llm`
📄 `src.nlp2cmd.llm.adaptive_learner` (21 functions, 4 classes)
📄 `src.nlp2cmd.llm.openrouter` (8 functions, 2 classes)
📄 `src.nlp2cmd.llm.repair` (7 functions, 2 classes)
📄 `src.nlp2cmd.llm.router` (22 functions, 3 classes)
📄 `src.nlp2cmd.llm.validator` (13 functions, 2 classes)
📄 `src.nlp2cmd.llm.vision` (9 functions, 2 classes)
📦 `src.nlp2cmd.monitoring`
📄 `src.nlp2cmd.monitoring.resources` (11 functions, 2 classes)
📄 `src.nlp2cmd.monitoring.token_costs` (10 functions, 2 classes)
📦 `src.nlp2cmd.nlp`
📄 `src.nlp2cmd.nlp.config` (19 functions, 4 classes)
📄 `src.nlp2cmd.nlp.entity_resolver` (17 functions, 2 classes)
📄 `src.nlp2cmd.nlp.intent_matcher` (10 functions, 3 classes)
📄 `src.nlp2cmd.nlp.normalizer` (13 functions, 2 classes)
📦 `src.nlp2cmd.nlp_enhanced` (14 functions, 2 classes)
📦 `src.nlp2cmd.nlp_light`
📄 `src.nlp2cmd.nlp_light.semantic_shell` (14 functions, 2 classes)
📄 `src.nlp2cmd.optimization_report`
📦 `src.nlp2cmd.orchestration`
📄 `src.nlp2cmd.orchestration.engine` (13 functions, 6 classes)
📄 `src.nlp2cmd.orchestration.handlers` (19 functions)
📄 `src.nlp2cmd.orchestration.metrics` (27 functions, 7 classes)
📄 `src.nlp2cmd.orchestration.reflection` (9 functions, 3 classes)
📦 `src.nlp2cmd.page_analysis`
📄 `src.nlp2cmd.page_analysis.base` (1 functions, 2 classes)
📄 `src.nlp2cmd.page_analysis.field_classifier` (4 functions, 1 classes)
📄 `src.nlp2cmd.page_analysis.form_analyzer` (7 functions, 1 classes)
📄 `src.nlp2cmd.page_analysis.iframe_analyzer` (2 functions, 1 classes)
📄 `src.nlp2cmd.page_analysis.link_extractor` (4 functions, 1 classes)
📄 `src.nlp2cmd.page_analysis.page_analyzer` (3 functions, 1 classes)
📦 `src.nlp2cmd.page_schema`
📄 `src.nlp2cmd.page_schema.base` (3 functions, 2 classes)
📄 `src.nlp2cmd.page_schema.button_extractor` (2 functions, 1 classes)
📄 `src.nlp2cmd.page_schema.copy_button_extractor` (2 functions, 1 classes)
📄 `src.nlp2cmd.page_schema.form_extractor` (2 functions, 1 classes)
📄 `src.nlp2cmd.page_schema.page_schema_extractor` (3 functions, 1 classes)
📄 `src.nlp2cmd.page_schema.radio_extractor` (2 functions, 1 classes)
📄 `src.nlp2cmd.page_schema.token_extractor` (2 functions, 1 classes)
📄 `src.nlp2cmd.parsing.toon_parser` (22 functions, 3 classes)
📄 `src.nlp2cmd.pipeline_runner` (2 functions, 2 classes)
📄 `src.nlp2cmd.pipeline_runner_browser` (3 functions, 1 classes)
📄 `src.nlp2cmd.pipeline_runner_desktop` (8 functions, 1 classes)
📄 `src.nlp2cmd.pipeline_runner_plans` (13 functions, 1 classes)
📄 `src.nlp2cmd.pipeline_runner_shell` (3 functions, 1 classes)
📄 `src.nlp2cmd.pipeline_runner_utils` (19 functions, 4 classes)
📦 `src.nlp2cmd.plan_execution`
📄 `src.nlp2cmd.plan_execution.browser_setup` (6 functions, 2 classes)
📄 `src.nlp2cmd.plan_execution.plan_executor` (17 functions, 1 classes)
📄 `src.nlp2cmd.plan_execution.step_orchestrator` (12 functions, 2 classes)
📦 `src.nlp2cmd.planner` (7 functions, 3 classes)
📄 `src.nlp2cmd.polish_support` (13 functions, 1 classes)
📦 `src.nlp2cmd.registry` (22 functions, 6 classes)
📦 `src.nlp2cmd.router` (11 functions, 4 classes)
📦 `src.nlp2cmd.schema_based`
📄 `src.nlp2cmd.schema_based.adapter`
📄 `src.nlp2cmd.schema_based.generator`
📄 `src.nlp2cmd.schema_driven` (8 functions, 2 classes)
📦 `src.nlp2cmd.schema_extraction`
📄 `src.nlp2cmd.schema_extraction.extractors` (10 functions, 5 classes)
📄 `src.nlp2cmd.schema_extraction.llm_extractor` (11 functions, 1 classes)
📄 `src.nlp2cmd.schema_extraction.python_extractors` (11 functions, 2 classes)
📄 `src.nlp2cmd.schema_extraction.registry` (11 functions, 1 classes)
📄 `src.nlp2cmd.schema_extraction.script_extractors` (6 functions, 2 classes)
📦 `src.nlp2cmd.schemas` (43 functions, 2 classes)
📦 `src.nlp2cmd.service` (11 functions, 4 classes)
📄 `src.nlp2cmd.service.cli` (1 functions)
📄 `src.nlp2cmd.service.docker_app`
📦 `src.nlp2cmd.skills` (1 functions)
📦 `src.nlp2cmd.skills.drawing`
📄 `src.nlp2cmd.skills.drawing.colors` (6 functions, 1 classes)
📄 `src.nlp2cmd.skills.drawing.commands` (19 functions, 8 classes)
📄 `src.nlp2cmd.skills.drawing.correction_engine` (9 functions, 5 classes)
📄 `src.nlp2cmd.skills.drawing.draw_object` (11 functions, 4 classes)
📄 `src.nlp2cmd.skills.drawing.event_store` (13 functions, 1 classes)
📄 `src.nlp2cmd.skills.drawing.events` (7 functions, 7 classes)
📄 `src.nlp2cmd.skills.drawing.navigation` (15 functions, 5 classes)
📄 `src.nlp2cmd.skills.drawing.nl_parser` (7 functions, 1 classes)
📄 `src.nlp2cmd.skills.drawing.object_fetcher` (13 functions, 6 classes)
📄 `src.nlp2cmd.skills.drawing.queries` (7 functions, 6 classes)
📦 `src.nlp2cmd.skills.drawing.renderers`
📄 `src.nlp2cmd.skills.drawing.renderers.base` (8 functions, 1 classes)
📄 `src.nlp2cmd.skills.drawing.renderers.playwright` (8 functions, 1 classes)
📄 `src.nlp2cmd.skills.drawing.renderers.svg` (8 functions, 1 classes)
📄 `src.nlp2cmd.skills.drawing.shapes` (38 functions, 35 classes)
📄 `src.nlp2cmd.skills.drawing.skill` (18 functions, 1 classes)
📄 `src.nlp2cmd.skills.drawing.text_to_shape` (9 functions, 3 classes)
📄 `src.nlp2cmd.skills.drawing.validation` (14 functions, 5 classes)
📄 `src.nlp2cmd.skills.drawing.visual_validator` (8 functions, 4 classes)
📦 `src.nlp2cmd.skills.search` (1 functions)
📄 `src.nlp2cmd.skills.search.engine` (20 functions, 3 classes)
📄 `src.nlp2cmd.skills.search.skill` (9 functions, 2 classes)
📦 `src.nlp2cmd.step_handlers`
📄 `src.nlp2cmd.step_handlers.base` (3 functions, 3 classes)
📄 `src.nlp2cmd.step_handlers.dispatcher` (4 functions, 1 classes)
📄 `src.nlp2cmd.step_handlers.drawing` (23 functions, 19 classes)
📄 `src.nlp2cmd.step_handlers.extraction` (10 functions, 8 classes)
📄 `src.nlp2cmd.step_handlers.interaction` (10 functions, 10 classes)
📄 `src.nlp2cmd.step_handlers.navigate` (2 functions, 1 classes)
📄 `src.nlp2cmd.step_handlers.registry` (7 functions, 1 classes)
📄 `src.nlp2cmd.step_handlers.session` (10 functions, 3 classes)
📦 `src.nlp2cmd.storage`
📄 `src.nlp2cmd.storage.per_command_store` (14 functions, 1 classes)
📄 `src.nlp2cmd.storage.versioned_store` (13 functions, 1 classes)
📦 `src.nlp2cmd.streams`
📄 `src.nlp2cmd.streams.base` (10 functions, 3 classes)
📄 `src.nlp2cmd.streams.ftp_stream` (4 functions, 1 classes)
📄 `src.nlp2cmd.streams.http_stream` (3 functions, 1 classes)
📄 `src.nlp2cmd.streams.libvirt_stream` (14 functions, 1 classes)
📄 `src.nlp2cmd.streams.rdp_stream` (3 functions, 1 classes)
📄 `src.nlp2cmd.streams.router` (7 functions, 1 classes)
📄 `src.nlp2cmd.streams.rtsp_stream` (17 functions, 1 classes)
📄 `src.nlp2cmd.streams.spice_stream` (3 functions, 1 classes)
📄 `src.nlp2cmd.streams.ssh_stream` (8 functions, 1 classes)
📄 `src.nlp2cmd.streams.vnc_stream` (7 functions, 1 classes)
📄 `src.nlp2cmd.streams.ws_stream` (8 functions, 1 classes)
📦 `src.nlp2cmd.thermodynamic` (25 functions, 10 classes)
📄 `src.nlp2cmd.thermodynamic.energy_models` (21 functions, 6 classes)
📦 `src.nlp2cmd.utils`
📄 `src.nlp2cmd.utils.data_files` (6 functions)
📄 `src.nlp2cmd.utils.external_cache` (13 functions, 1 classes)
📄 `src.nlp2cmd.utils.playwright_installer` (6 functions)
📄 `src.nlp2cmd.utils.yaml_compat`
📦 `src.nlp2cmd.validators` (25 functions, 8 classes)
📦 `src.nlp2cmd.web_schema`
📄 `src.nlp2cmd.web_schema.browser_config` (23 functions, 2 classes)
📄 `src.nlp2cmd.web_schema.extractor` (10 functions, 3 classes)
📄 `src.nlp2cmd.web_schema.form_data_loader` (47 functions, 1 classes)
📄 `src.nlp2cmd.web_schema.form_handler` (9 functions, 3 classes)
📄 `src.nlp2cmd.web_schema.history` (15 functions, 2 classes)
📄 `src.nlp2cmd.web_schema.site_explorer` (34 functions, 3 classes)
📄 `test_nlp2cmd_commands` (18 functions)
📄 `test_nlp2cmd_enhanced` (14 functions)
📄 `test_screenshots.analiza_workflow`
📄 `test_screenshots.analyze_screenshots` (4 functions)
📄 `test_screenshots.capture_script`
📄 `test_screenshots.compare_screenshots` (4 functions)
📄 `test_screenshots.raport_testu`
📄 `test_screenshots.test_openrouter_workflow` (4 functions)
📄 `tools.analysis.analyze_version_detection` (6 functions)
📄 `tools.analysis.compare_batches` (1 functions)
📄 `tools.analysis.compare_llm` (1 functions)
📄 `tools.generation.generate_cmd_from_prompts` (5 functions, 1 classes)
📄 `tools.generation.generate_cmd_simple` (4 functions)
📄 `tools.generation.intelligent_command_generator` (18 functions, 3 classes)
📄 `tools.manual_tests.quick_test_nlp2cmd` (1 functions)
📄 `tools.schema.cmd2schema` (9 functions, 1 classes)
📄 `tools.schema.comprehensive_command_scanner` (24 functions, 3 classes)
📄 `tools.schema.enhanced_schema_generator` (37 functions, 3 classes)
📄 `tools.schema.intelligent_schema_generator` (14 functions, 2 classes)
📄 `tools.schema.non_llm_schema_extractor` (28 functions, 3 classes)
📄 `tools.schema.update_schemas` (3 functions)
📄 `tools.schema.validate_schemas` (1 functions)
📄 `tree`

## Requirements

- Python >= 3.11
- pyyaml >=6.0- pydantic >=2.0- rich >=13.0- click >=8.0- httpx >=0.25.0- jinja2 >=3.0- jsonschema >=4.0- python-dotenv >=1.0- watchdog >=3.0- numpy >=1.24.0- psutil >=5.9.0- rapidfuzz >=3.0

## Contributing

**Contributors:**
- Tom Softreck <tom@sapletta.com>
- Tom Sapletta <tom-sapletta-com@users.noreply.github.com>

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.
### Development Setup

```bash
# Clone the repository
git clone https://github.com/wronai/nlp2cmd
cd nlp2cmd

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Documentation

- 🤝 [Contributing](./CONTRIBUTING.md) — Contribution guidelines
- 💡 [Examples](./examples) — Usage examples and code samples

### Generated Files

| Output | Description | Link |
|--------|-------------|------|
| `README.md` | Project overview (this file) | — |
| `CONTRIBUTING.md` | Contribution guidelines | [View](./CONTRIBUTING.md) |
| `examples` | Usage examples and code samples | [View](./examples) |

<!-- code2docs:end -->
