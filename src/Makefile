TESTRUN = nosetests
DEBUGOPTS = -v -x
LOGFILTER = --logging-filter=SCTA_repo.src.unittests
PROGRESSOPTS = -v --nologcapture
TESTDIR = unittests
PROGRESSDIR = unittests/test-progress

.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  SFU_Test              to run through all SFU unittests in debug mode"
	@echo "  SFU_Progress          write all SFU unittests results to a progress log"
	@echo "  System_Test           to run through all System unittests in debug mode"
	@echo "  System_Progress       write all System unittests results to a progress log"
	@echo "  DataLogging_Test      to run through all DataLogging unittests in debug mode"
	@echo "  DataLogging_Progress  write all DataLogging unittests results to a progress log"
	@echo "  SFU_Test              to run through all SFU unittests in debug mode"
	@echo "  SFU_Progress          write all SFU unittests results to a progress log"
	@echo "  FSW_Test              to run through all FSW unittests in debug mode"
	@echo "  FSW_Progress          write all FSW unittests results to a progress log"
	@echo "  Fastbit_Test          to run through all Fastbit unittests in debug mode"
	@echo "  Fastbit_Progress      write all Fastbit unittests results to a progress log"
	@echo "  Fireberd_Test         to run through all Fireberd unittests in debug mode"
	@echo "  Fireberd_Progress     write all Fireberd unittests results to a progress log"
	@echo "  SLG_Test              to run through all SLG unittests in debug mode"
	@echo "  SLG_Progress          write all SLG unittests results to a progress log"

.PHONY: init
init:
	pip install -r requirements.txt

.PHONY: test_all
test_all:
	$(TESTRUN) $(DEBUGOPTS) $(TESTDIR)

.PHONY: System_Test
System_Test:
	$(TESTRUN) $(DEBUGOPTS) $(LOGFILTER),SCTA.System $(TESTDIR)/System_Test.py

.PHONY: System_Progress
System_Progress:
	$(TESTRUN) $(PROGRESSOPTS) $(TESTDIR)/System_Test.py 2> $(PROGRESSDIR)/System_Test-log.txt

.PHONY: DataLogging_Test
DataLogging_Test:
	$(TESTRUN) $(DEBUGOPTS) $(LOGFILTER),SCTA.DataLogging $(TESTDIR)/DataLogging_Test.py

.PHONY: DataLogging_Progress
DataLogging_Progress:
	$(TESTRUN) $(PROGRESSOPTS) $(TESTDIR)/DataLogging_Test.py 2> $(PROGRESSDIR)/DataLogging_Test-log.txt

.PHONY: SFU_Test
SFU_Test:
	$(TESTRUN) $(DEBUGOPTS) $(LOGFILTER),SCTA.Instrumentation $(TESTDIR)/SFU_Test.py

.PHONY: SFU_Progress
SFU_Progress:
	$(TESTRUN) $(PROGRESSOPTS) $(TESTDIR)/SFU_Test.py 2> $(PROGRESSDIR)/SFU_Test-log.txt

.PHONY: FSW_Test
FSW_Test:
	$(TESTRUN) $(DEBUGOPTS) $(LOGFILTER),SCTA.Instrumentation $(TESTDIR)/FSW_Test.py

.PHONY: FSW_Progress
FSW_Progress:
	$(TESTRUN) $(PROGRESSOPTS) $(TESTDIR)/FSW_Test.py 2> $(PROGRESSDIR)/FSW_Test-log.txt

.PHONY: Fastbit_Test
Fastbit_Test:
	$(TESTRUN) $(DEBUGOPTS) $(LOGFILTER),SCTA.Instrumentation $(TESTDIR)/Fastbit_Test.py

.PHONY: Fastbit_Progress
Fastbit_Progress:
	$(TESTRUN) $(PROGRESSOPTS) $(TESTDIR)/Fastbit_Test.py 2> $(PROGRESSDIR)/Fastbit_Test-log.txt

.PHONY: Fireberd_Test
Fireberd_Test:
	$(TESTRUN) $(DEBUGOPTS) $(LOGFILTER),SCTA.Instrumentation $(TESTDIR)/Fireberd_Test.py

.PHONY: Fireberd_Progress
Fireberd_Progress:
	$(TESTRUN) $(PROGRESSOPTS) $(TESTDIR)/Fireberd_Test.py 2> $(PROGRESSDIR)/Fireberd_Test-log.txt

.PHONY: SLG_Test
SLG_Test:
	$(TESTRUN) $(DEBUGOPTS) $(LOGFILTER),SCTA.Instrumentation $(TESTDIR)/SLG_Test.py

.PHONY: SLG_Progress
SLG_Progress:
	$(TESTRUN) $(PROGRESSOPTS) $(TESTDIR)/SLG_Test.py 2> $(PROGRESSDIR)/SLG_Test-log.txt