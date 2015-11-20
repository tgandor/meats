using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

internal struct MoveOperation
{
    public string TargetFolder { get; set; }
    public List<string>  FilesToMove { get; set; }
}

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

            var results = Directory.EnumerateFiles(directory)
                .Where(f => Path.GetFileName(f).Length >= 8)
                .GroupBy(f => Path.GetFileName(f).Substring(0, 8), f => f, (key, g) => new MoveOperation()
            {
                TargetFolder = key,
                FilesToMove = g.ToList()
            });

            var level2 = results.GroupBy(row => row.TargetFolder.Substring(0, 6), row => row, (key, group) => new
            {
                FolderAbove = key,
                MoveOperations = group
            });

            foreach (var folderGroup in level2)
            {
                var listSubfolders = folderGroup.MoveOperations.OrderBy(moveOp => moveOp.TargetFolder).ToList();
                int packNumber = 1;
                while (listSubfolders.Count > 0)
                {
                    var subfolder = string.Format("{0}-{1}", folderGroup.FolderAbove, packNumber);
                    ++packNumber;
                    var targetPrefix = Path.Combine(directory, subfolder);
                    if (!Directory.Exists(targetPrefix))
                    {
                        Directory.CreateDirectory(targetPrefix);
                    }                    

                    int numToTake = listSubfolders.Count > 11 ? 10 : listSubfolders.Count;
                    var portion = listSubfolders.GetRange(0, numToTake);
                    listSubfolders = listSubfolders.GetRange(numToTake, listSubfolders.Count - numToTake);

                    MoveFilesToDirectory(portion, targetPrefix);
                }
            }
            
            Die(0);
        }

        private static void MoveFilesToDirectory(IEnumerable<MoveOperation> results, string directory)
        {
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
        }
    }
}
