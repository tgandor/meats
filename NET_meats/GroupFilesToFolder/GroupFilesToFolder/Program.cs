using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GroupFilesToFolder
{
    class Program
    {
        static private void Die(int returnCode)
        {
            Console.Write("Press Enter to exit... ");
            Console.ReadLine();
            Environment.Exit(returnCode);           
        }

        static void Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.WriteLine("No argument specified. Please pass directory to split into 8-char subfolders.");
                Die(1);
            }

            var directory = args.Length > 0 ? args[0] : ".";

            Console.WriteLine("This will process directory '{0}'.", directory);
            Console.Write("Type 'yes' to continue: ");
            if (Console.ReadLine() != "yes")
            {
                Console.WriteLine("Operation cancelled.");
                Die(2);
            }

            Console.WriteLine("Reading directory files...");

            var results = Directory.EnumerateFiles(directory).GroupBy(f => Path.GetFileName(f).Substring(0, 8), f => f, (key, g) => new
            {
                TargetFolder = key,
                FilesToMove = g.ToList()
            });

            foreach (var moveOperation in results)
            {
                var targetFolder = Path.Combine(directory, moveOperation.TargetFolder);
                Console.WriteLine("Folder: {0}", moveOperation.TargetFolder);
                if (!Directory.Exists(targetFolder))
                {
                    Directory.CreateDirectory(targetFolder);
                }
                foreach (var file in moveOperation.FilesToMove)
                {
                    var targetFile = Path.Combine(targetFolder, Path.GetFileName(file));
                    File.Move(file, targetFile);
                    Console.WriteLine("  {0} -> {1}", file, targetFile);
                }
            }

            Die(0);
        }
    }
}
