using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using SolutionLibrary;

namespace FindLostProjects
{
    internal class Program
    {
        private static void Dump<T>(IEnumerable<T> list, string glue = "\n")
        {
            Console.WriteLine(string.Join(glue, list.Select(x => x.ToString())));
        }

        private static IEnumerable<string> ProjectRelativePaths(string solutionFileName)
        {
            if (!File.Exists(solutionFileName))
            {
                Console.Error.WriteLine("File not found: {0}", solutionFileName);
                return Enumerable.Empty<string>();
            }

            var solution = new Solution(solutionFileName);
            return solution.Projects.Select(x => x.RelativePath);
        }

        private static bool AssertFileExists(string path)
        {
            if (File.Exists(path))
            {
                return true;
            }
            Console.Error.WriteLine("Error: File not found: {0}", path);
            return false;
        }

        private static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.Error.WriteLine("Usage: FindLostProjects.exe <solution_file>...");
                return;
            }

            if (!args.All(AssertFileExists))
            {
                return;
            }

            // maybe TODO: consider paths of solutions other than first
            var solutionDirectory = Path.GetDirectoryName(args[0]);
            if (!string.IsNullOrEmpty(solutionDirectory))
            {
                Directory.SetCurrentDirectory(solutionDirectory);
            }

            Console.WriteLine("Working in: {0}", Directory.GetCurrentDirectory());

            var projectsOnDisk = Directory.GetFiles(".", "*.*proj", SearchOption.AllDirectories)
                .Select(x => x.Replace(".\\", ""))
                .Where(x => !x.EndsWith(".proj"));

            var projectsInSolution = args.SelectMany(ProjectRelativePaths);

            var lostProjects = projectsOnDisk.Except(projectsInSolution);

            Console.WriteLine("Lost projects:");
            Dump(lostProjects);
        }
    }
}
