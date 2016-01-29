using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using SolutionLibrary;

namespace SearchSolutionForProject
{
    internal class Program
    {
        private static int numResults;

        private static void SearchSolution(string phrase, string solutionFileName)
        {
            if (!File.Exists(solutionFileName))
            {
                Console.Error.WriteLine("Solution file not found: {0}", solutionFileName);
                return;
            }

            var solution = new Solution(solutionFileName);

            var projectsByGuid = solution.Projects.ToDictionary(x => x.ProjectGuid);

            foreach (var solutionProject in solution.Projects)
            {
                if (!solutionProject.ProjectName.Contains(phrase)) continue;

                var path = new Stack<string>();
                path.Push(solutionProject.ProjectName);
                var parent = solutionProject;
                while (!string.IsNullOrEmpty(parent.ParentProjectGuid))
                {
                    if (!projectsByGuid.TryGetValue(parent.ParentProjectGuid, out parent))
                    {
                        Console.Error.WriteLine("\nError: parent project of {0} (guid {1}) not found.",
                            parent.ProjectName, parent.ParentProjectGuid);
                        path.Push("?");
                        break;
                    }

                    path.Push(parent.ProjectName);
                }

                Console.WriteLine(
                    "\n{5}\nProject: {1}\n  Solution: {0}\n  Logical:  {2}\n  Physical: {3}\n  Type:     {4}",
                    solutionFileName,
                    solutionProject.ProjectName, string.Join("/", path), solutionProject.AbsolutePath,
                    solutionProject.ProjectType, ++numResults);
            }
        }

        private static void Main(string[] args)
        {
            if (args.Length < 2)
            {
                Console.Error.WriteLine("Usage: SearchSolutionForProject.exe <search_phrase> <solution_file>...");
                return;
            }

            foreach (var solutionFile in args.Skip(1))
            {
                SearchSolution(args[0], solutionFile);
            }
        }
    }
}
