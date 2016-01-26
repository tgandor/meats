using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace FindLostProjects
{
    class Program
    {
        static void dump<T>(IEnumerable<T> list)
        {
            Console.WriteLine(string.Join("\n", list.Select(x => x.ToString())));
        }

        static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.Error.WriteLine("Usage: FindLostProjects.exe <solution_file>");
                return;
            }

            if (!File.Exists(args[0]))
            {
                Console.Error.WriteLine("File not found: {0}", args[0]);
                return;
            }

            var solutionDirectory = Path.GetDirectoryName(args[0]);
            if (solutionDirectory != "")
            {
                Directory.SetCurrentDirectory(solutionDirectory);
            }
                
            Console.WriteLine("Working in: {0}", Directory.GetCurrentDirectory());

            var projectsOnDisk = Directory.GetFiles(".", "*.*proj", SearchOption.AllDirectories)
                .Select(x => x.Replace(".\\", ""))
                .Where(x => !x.EndsWith(".proj"));

            var solution = new Solution(args[0]);
            var projectsInSolution = solution.Projects.Select(x => x.RelativePath);

            var lostProjects = projectsOnDisk.Except(projectsInSolution);

            Console.WriteLine("Lost projects:");
            dump(lostProjects);
        }
    }
}
