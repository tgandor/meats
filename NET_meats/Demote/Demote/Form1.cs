using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Security.Principal;
using System.Text;
using System.Windows.Forms;
using System.Diagnostics;

namespace Demote
{

    public partial class Form1 : Form
    {
        private int total = 0;

        public Form1()
        {
            InitializeComponent();
            notifyIcon1.Text = "Demoting Processes";
            notifyIcon1.Visible = true;
            if (!AreWeElevated())
            {
                notifyIcon1.ShowBalloonTip(3500, "Process Not Elevated", 
                    "Accessing processes from other users may fail.", ToolTipIcon.Warning);
            }
            Process.GetCurrentProcess().PriorityClass = ProcessPriorityClass.BelowNormal;
        }

        public static bool AreWeElevated()
        {
            // bool value to hold our return value
            bool isAdmin;
            try
            {
                //get the currently logged in user
                WindowsIdentity user = WindowsIdentity.GetCurrent();
                WindowsPrincipal principal = new WindowsPrincipal(user);
                isAdmin = principal.IsInRole(WindowsBuiltInRole.Administrator);
            }
            catch (UnauthorizedAccessException)
            {
                isAdmin = false;
            }
            catch (Exception)
            {
                isAdmin = false;
            }
            return isAdmin;
        }

        private static int _demote(Process proc)
        {
            try
            {
                if (proc.PriorityClass == ProcessPriorityClass.Normal)
                {
                    proc.PriorityClass = ProcessPriorityClass.BelowNormal;
                    if (proc.PriorityClass == ProcessPriorityClass.BelowNormal)
                    {
                        return 1;
                    }
                    else
                    {
                        return -1;
                    }
                }
                return 0;
            }
            catch (Exception)
            {
                return -1;
            }            
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (listBox1.Items.Count == 0)
            {
                toolStripStatusLabel1.Text = "No processes to monitor.";
                return;
            }
            toolStripStatusLabel1.Text = "Checking processes...";
            int found = 0;
            int demoted = 0;
            int failed = 0;
            foreach (string name in listBox1.Items)
            {
                foreach (Process proc in Process.GetProcessesByName(name))
                {
                    ++found;
                    switch (_demote(proc))
                    {
                        case -1:
                            ++failed;
                            break;
                        case 1:
                            ++demoted;
                            ++total;
                            break;
                    }
                }
            }
            toolStripStatusLabel1.Text = String.Format("{0}: {1} processes, {2} demoted ({4} total), {3} failed.", 
                DateTime.Now.ToString("HH:mm:ss"), found, demoted, failed, total);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            while (listBox1.SelectedItems.Count > 0)
            {
                listBox1.Items.Remove(listBox1.SelectedItems[0]);
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            button4.Enabled = true;
            button3.Enabled = false;
            timer1.Enabled = false;
            toolStripStatusLabel1.Text = "Paused";
        }

        private void button4_Click(object sender, EventArgs e)
        {
            button3.Enabled = true;
            button4.Enabled = false;
            timer1.Enabled = true;
            toolStripStatusLabel1.Text = "Monitoring";
        }

        private void listBox1_SelectedValueChanged(object sender, EventArgs e)
        {
            button1.Enabled = listBox1.SelectedIndices.Count > 0;
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            button2.Enabled = textBox1.Text.Length > 0;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            listBox1.Items.Add(textBox1.Text);
            textBox1.Clear();
        }

        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            if (notifyIcon1 != null)
            {
                notifyIcon1.Visible = false;
                notifyIcon1.Dispose();
                notifyIcon1 = null;
            }
        }

        private void notifyIcon1_MouseClick(object sender, MouseEventArgs e)
        {
            WindowState = WindowState == FormWindowState.Minimized 
                ? FormWindowState.Normal 
                : FormWindowState.Minimized;
        }
    }
}
