# FindLostProjects suite

This solution includes a few (3 at time of writing) command line tools to examine Visual Studio Solution (.sln) files.

## FindLostProjects.exe

`Usage: FindLostProjects.exe <solution_file>...`

This program searches the filesytem for project files (`*.*proj`) and lists the "lost projects", i.e. projects which are not included in the solution(s).

## CheckSolution.exe

`Usage: CheckSolution.exe <solution_file>...`

Parses the solution and checks if the referenced projects (except for projects of type "Solution Folder") are present in the filesytem. This could also be done by opening the file and receiving errors loading the projects, but the command line tools scales better.

## SearchSolutionForProject.exe

`Usage: SearchSolutionForProject.exe <search_phrase> <solution_file>...`

Looks for projects whose names contain the phrase given as first argument.
It presents the results with a counter, and some information, for example like these:

```
C:\> SearchSolutionForProject.exe test Solution.sln

1
Project: Database tests
  Solution: Solution.sln
  Logical:  Tests/Database test
  Physical: Database tests
  Type:     SolutionFolder

(...)
```
