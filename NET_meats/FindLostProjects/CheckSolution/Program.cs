using System;
using System.IO;
using SolutionLibrary;

namespace CheckSolution
{
    internal class Program
    {
        private static void CheckSolution(string solutionFileName)
        {
            if (!File.Exists(solutionFileName))
            {
                Console.Error.WriteLine("File not found: {0}", solutionFileName);
                return;
            }

            var error = false;

            var solution = new Solution(solutionFileName);

            foreach (var solutionProject in solution.Projects)
            {
                if (solutionProject.ProjectType == "SolutionFolder" || File.Exists(solutionProject.AbsolutePath))
                    continue;
                Console.WriteLine("\n{0}: project \n  '{1}'\n  - not found on disk.", solutionFileName,
                    solutionProject.RelativePath);
                error = true;
            }

            if (!error)
            {
                Console.WriteLine("\n{0}: OK.", solutionFileName);
            }
        }

        private static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.Error.WriteLine("Usage: CheckSolution.exe <solution_file>...");
                return;
            }

            foreach (var solutionFile in args)
            {
                CheckSolution(solutionFile);
            }
        }
    }
}
