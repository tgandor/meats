using System;
using System.Runtime.InteropServices;

namespace GetpidPInvokr
{
	class MainClass
	{
		[DllImport ("libc.so.6")]
		private static extern int getpid();

		public static void Main (string[] args)
		{
			Console.WriteLine ("Hello World! My pid is: " + getpid());
		}
	}
}
