using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;

// this code comes from here:
// https://social.msdn.microsoft.com/Forums/en-US/6ac84a8a-6b5b-40d5-adfc-38e978d6cdbe/parsing-a-visual-studio-solution-file-in-the-c-code
// and originally here:
// http://stackoverflow.com/questions/707107/parsing-visual-studio-solution-files

namespace SolutionLibrary
{
    public class Solution
    {
        //internal class SolutionParser
        //Name: Microsoft.Build.Construction.SolutionParser
        //Assembly: Microsoft.Build, Version=4.0.0.0

        private static readonly Type s_SolutionParser;
        private static readonly PropertyInfo s_SolutionParser_solutionReader;
        private static readonly MethodInfo s_SolutionParser_parseSolution;
        private static readonly PropertyInfo s_SolutionParser_projects;

        static Solution()
        {
            s_SolutionParser =
                Type.GetType(
                    "Microsoft.Build.Construction.SolutionParser, Microsoft.Build, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a",
                    false, false);
            if (s_SolutionParser != null)
            {
                s_SolutionParser_solutionReader = s_SolutionParser.GetProperty("SolutionReader",
                    BindingFlags.NonPublic | BindingFlags.Instance);
                s_SolutionParser_projects = s_SolutionParser.GetProperty("Projects",
                    BindingFlags.NonPublic | BindingFlags.Instance);
                s_SolutionParser_parseSolution = s_SolutionParser.GetMethod("ParseSolution",
                    BindingFlags.NonPublic | BindingFlags.Instance);
            }
        }

        public Solution(string solutionFileName)
        {
            if (s_SolutionParser == null)
            {
                throw new InvalidOperationException(
                    "Can not find type 'Microsoft.Build.Construction.SolutionParser' are you missing a assembly reference to 'Microsoft.Build.dll'?");
            }
            var solutionParser =
                s_SolutionParser.GetConstructors(BindingFlags.Instance | BindingFlags.NonPublic).First().Invoke(null);
            using (var streamReader = new StreamReader(solutionFileName))
            {
                s_SolutionParser_solutionReader.SetValue(solutionParser, streamReader, null);
                s_SolutionParser_parseSolution.Invoke(solutionParser, null);
            }
            var array = (Array) s_SolutionParser_projects.GetValue(solutionParser, null);
            var projects = (from object value in array select new SolutionProject(value)).ToList();
            Projects = projects;
        }

        public List<SolutionProject> Projects { get; private set; }
    }

    [DebuggerDisplay("{ProjectName}, {RelativePath}, {ProjectGuid}")]
    public class SolutionProject
    {
        private static readonly Type s_ProjectInSolution;
        private static readonly PropertyInfo s_ProjectInSolution_ProjectName;
        private static readonly PropertyInfo s_ProjectInSolution_RelativePath;
        private static readonly PropertyInfo s_ProjectInSolution_AbsolutePath;
        private static readonly PropertyInfo s_ProjectInSolution_ProjectGuid;
        private static readonly PropertyInfo s_ProjectInSolution_ParentProjectGuid;
        private static readonly PropertyInfo s_ProjectInSolution_ProjectType;
        private readonly object solutionProject_;

        static SolutionProject()
        {
            // https://msdn.microsoft.com/en-us/library/microsoft.build.construction.projectinsolution.aspx
            s_ProjectInSolution =
                Type.GetType(
                    "Microsoft.Build.Construction.ProjectInSolution, Microsoft.Build, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a",
                    false, false);
            if (s_ProjectInSolution != null)
            {
                s_ProjectInSolution_ProjectName = s_ProjectInSolution.GetProperty("ProjectName",
                    BindingFlags.NonPublic | BindingFlags.Instance);
                s_ProjectInSolution_RelativePath = s_ProjectInSolution.GetProperty("RelativePath",
                    BindingFlags.NonPublic | BindingFlags.Instance);
                s_ProjectInSolution_AbsolutePath = s_ProjectInSolution.GetProperty("AbsolutePath",
                    BindingFlags.NonPublic | BindingFlags.Instance);
                s_ProjectInSolution_ProjectGuid = s_ProjectInSolution.GetProperty("ProjectGuid",
                    BindingFlags.NonPublic | BindingFlags.Instance);
                s_ProjectInSolution_ParentProjectGuid = s_ProjectInSolution.GetProperty("ParentProjectGuid",
                    BindingFlags.NonPublic | BindingFlags.Instance);
                s_ProjectInSolution_ProjectType = s_ProjectInSolution.GetProperty("ProjectType",
                    BindingFlags.NonPublic | BindingFlags.Instance);
            }
        }

        public SolutionProject(object solutionProject)
        {
            solutionProject_ = solutionProject;
            ProjectName = s_ProjectInSolution_ProjectName.GetValue(solutionProject, null) as string;
            RelativePath = s_ProjectInSolution_RelativePath.GetValue(solutionProject, null) as string;
            ProjectGuid = s_ProjectInSolution_ProjectGuid.GetValue(solutionProject, null) as string;
            ParentProjectGuid = s_ProjectInSolution_ParentProjectGuid.GetValue(solutionProject, null) as string;
            ProjectType = s_ProjectInSolution_ProjectType.GetValue(solutionProject, null).ToString();
        }

        public string ProjectName { get; private set; }
        public string RelativePath { get; private set; }

        public string AbsolutePath
        {
            // Sometimes there is no absolute path...
            get { return s_ProjectInSolution_RelativePath.GetValue(solutionProject_, null) as string; }
        }

        public string ProjectGuid { get; private set; }
        public string ParentProjectGuid { get; private set; }
        public string ProjectType { get; private set; }
    }
}
