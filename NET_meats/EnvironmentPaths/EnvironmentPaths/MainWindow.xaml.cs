using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace EnvironmentPaths
{
	/// <summary>
	/// Interaction logic for MainWindow.xaml
	/// </summary>
	public partial class MainWindow : Window
	{
		public MainWindow()
		{
			InitializeComponent();
			LoadVariables();
		}

		private void LoadVariables()
		{
			var varNames = System.Environment.GetEnvironmentVariables().Keys.Cast<string>();
			cbVariable.ItemsSource = varNames.OrderBy(s => s);
		}

		private void cbVariable_SelectionChanged(object sender, SelectionChangedEventArgs e)
		{
			var name = cbVariable.SelectedValue as string;
			var value = System.Environment.GetEnvironmentVariable(name);
			var splitText = value.Replace(';', '\n');
			tbSplitVariable.Text = splitText;
		}
	}
}
