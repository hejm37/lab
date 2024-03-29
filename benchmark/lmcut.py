#! /usr/bin/env python

"""Solve some tasks with A* and the LM-Cut heuristic."""

import os
import os.path
import platform

from lab.environments import LocalEnvironment, BaselSlurmEnvironment

from downward.experiment import FastDownwardExperiment
from downward.reports.absolute import AbsoluteReport
from downward.reports.scatter import ScatterPlotReport


ATTRIBUTES = ['coverage', 'error', 'expansions', 'total_time']

NODE = platform.node()
if NODE.endswith(".scicore.unibas.ch") or NODE.endswith(".cluster.bc2.ch"):
    # Create bigger suites with suites.py from the downward-benchmarks repo.
    SUITE = ['depot', 'freecell', 'gripper', 'zenotravel']
    ENV = BaselSlurmEnvironment(email="my.name@unibas.ch")
else:
    SUITE = ['depot']
    # SUITE = ["agricola", "Barman", "caldera", "caldera-split", "CaveDiving", "Childsnack", "CityCar", "data-network", "flashfill", "Floortile", "GED", "Hiking", "Maintenance", "nurikabe", "Openstacks", "organic-synthesis", "organic-synthesis-split", "Parking", "settlers", "snake", "spider", "termes", "Tetris", "Thoughtful", "Transport", "Visitall"]
    ENV = LocalEnvironment(processes=8)
# Use path to your Fast Downward repository.
REPO = os.environ["DOWNWARD_REPO"]
BENCHMARKS_DIR = os.environ["DOWNWARD_BENCHMARKS"]
REVISION_CACHE = os.path.expanduser('~/lab/revision-cache')

exp = FastDownwardExperiment(environment=ENV, revision_cache=REVISION_CACHE)

# Add built-in parsers to the experiment.
exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(exp.TRANSLATOR_PARSER)
exp.add_parser(exp.SINGLE_SEARCH_PARSER)
exp.add_parser(exp.PLANNER_PARSER)

exp.add_suite(BENCHMARKS_DIR, SUITE)
exp.add_algorithm(
    'blind', REPO, 'default', ['--search', 'astar(blind())'],
    driver_options=['--overall-time-limit', '5m',
     '--overall-memory-limit', '8192M'])
exp.add_algorithm(
    'lmcut', REPO, 'default', ['--search', 'astar(lmcut())'],
    driver_options=['--overall-time-limit', '5m',
     '--overall-memory-limit', '8192M'])
exp.add_algorithm(
    'ff', REPO, 'default',
    ['--search', 'lazy_greedy([ff()])'],
    driver_options=['--overall-time-limit', '5m',
     '--overall-memory-limit', '8192M'])
exp.add_algorithm(
    'ff_preferred', REPO, 'default',
    ['--search', 'lazy_greedy([ff()], preferred=[ff()])'],
    driver_options=['--overall-time-limit', '5m',
     '--overall-memory-limit', '8192M'])
exp.add_algorithm(
    'lama-2011', REPO, 'default', [],
    driver_options=['--alias', 'seq-sat-lama-2011',
                    '--overall-time-limit', '5m',
                    '--overall-memory-limit', '8192M'])

# Add step that writes experiment files to disk.
exp.add_step('build', exp.build)

# Add step that executes all runs.
exp.add_step('start', exp.start_runs)

# Add step that collects properties from run directories and
# writes them to *-eval/properties.
exp.add_fetcher(name='fetch')

# Add report step (AbsoluteReport is the standard report).
exp.add_report(
    AbsoluteReport(attributes=ATTRIBUTES), outfile='report.html')

# Add scatter plot report step.
exp.add_report(
    ScatterPlotReport(
        attributes=["expansions"], filter_algorithm=["blind", "lmcut", "ff", "ff_preferred", "lama-2011"]),
    outfile='scatterplot.png')

# Parse the commandline and show or run experiment steps.
exp.run_steps()
