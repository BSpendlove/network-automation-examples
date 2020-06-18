using System;
using System.Text.RegularExpressions;
using System.Threading;
using Renci.SshNet;

namespace Example4
{
    class Program
    {
        static void Main(string[] args)
        {
            CiscoSSH _ssh = new CiscoSSH("192.168.0.252", "cisco", "ciscodisco", "ciscodisco", 22);
            _ssh.Disconnect();
        }
    }

    class CiscoSSH
    {
        public string IP {get; set; }
        public string Username { get; set; }
        public string Password { get; set; }

        public string Secret { get; set; }
        public int Port { get; set; }

        private SshClient ssh_session { get; set; }

        private ShellStream shell_stream { get; set; }

        public string base_prompt { get; set; }

        public int global_delay { get; set; }

        public CiscoSSH(string ip, string username, string password, string secret, int port)
        {
            this.IP = ip;
            this.Username = username;
            this.Password = password;
            this.Secret = secret;
            this.Port = port;
            
            this.global_delay = 200;
            EstablishSession();
            SessionPreparation();
            System.Console.WriteLine(EnableMode("enable"));
            System.Console.WriteLine(SendCommand("show version"));
        }

        public void EstablishSession()
        {
            this.ssh_session = new SshClient(
                this.IP,
                this.Port,
                this.Username,
                this.Password
            );

            if (!this.ssh_session.IsConnected)
            {
                this.ssh_session.Connect();
                this.CreateShell();
            }
        }

        public void SessionPreparation()
        {
            SetPrompt();
            DisablePaging();
        }

        public string EnableMode(string command="", string pattern="ssword")
        {
            WriteChannel(NormalizeCommand(command));

            string output = ReadChannelUntil(pattern);
            WriteChannel(NormalizeCommand(this.Secret));
            output += ReadChannelUntil();

            return output;
        }

        public void CreateShell()
        {
            shell_stream = ssh_session.CreateShellStream("dumb", 80, 24, 800, 600, 1024);
        }

        public string DisablePaging(string cmd_length="terminal length 0", string cmd_width="terminal width 0")
        {
            float loop_delay = 0.2f;
            int sleep_delay = Convert.ToInt32(loop_delay * global_delay);
            shell_stream.Flush();
            Thread.Sleep(sleep_delay);
            string output = "";
            output += SendCommand(cmd_length);
            output += SendCommand(cmd_width);
            return output;
        }

        public string FindPrompt()
        {
            string prompt = "";
            int local_counter = 0;

            WriteChannel("\n");

            prompt = ReadChannel().Trim();

            while(String.IsNullOrEmpty(prompt) && local_counter < 10)
            {
                prompt = ReadChannel().Trim();

                if(String.IsNullOrEmpty(prompt))
                {
                    WriteChannel("\n");
                    local_counter += 1;
                }

                local_counter += 1;
                Thread.Sleep(Convert.ToInt32(global_delay * 0.1f));
            }

            if(String.IsNullOrEmpty(prompt))
            {
                throw new ApplicationException("Could not find prompt...");
            }

            return prompt;
        }

        public void SetPrompt(string pattern=">")
        {
            string prompt = FindPrompt();

            if(String.IsNullOrEmpty(pattern))
            {
                this.base_prompt = prompt;
            }
            else
            {
                var regexMatch = Regex.Match(prompt, pattern);
                if(regexMatch.Success)
                {
                    this.base_prompt = prompt.Substring(0, prompt.Length - regexMatch.Length);
                }
                else
                {
                    throw new ApplicationException("Unable to Set Prompt...");
                }
            }
        }

        public string SendCommand(string command="", string pattern="", int max_loops=300, bool cmd_verify=true)
        {
            bool foundPattern = false;
            float loop_delay = 0.2f;
            int sleep_delay = Convert.ToInt32(loop_delay * global_delay);

            if(String.IsNullOrEmpty(pattern))
            {
                pattern = this.base_prompt;
            }
            else
            {
                pattern = pattern.Trim();
            }

            string cmd = command.Trim();

            Thread.Sleep(sleep_delay);
            WriteChannel(NormalizeCommand(cmd));

            string output  = "";
            string new_data = "";
            if(!String.IsNullOrEmpty(cmd))
            {
                new_data += ReadChannelUntil(cmd);

                if(new_data.Contains(cmd))
                {
                    new_data += "\n";
                }
            }

            for(int i = 0; i < max_loops; i++)
            {

                if(!String.IsNullOrEmpty(new_data))
                {
                    output += new_data;

                    var regexMatch = Regex.Match(new_data, pattern, RegexOptions.IgnoreCase);
                    if(regexMatch.Success)
                    {
                        foundPattern = true;
                        break;
                    }
                }

                new_data += ReadChannel();
                Thread.Sleep(sleep_delay);
            }

            if(!foundPattern)
            {
                throw new ApplicationException("Could not find pattern in data");
            }

            return output;
        }

        public string NormalizeCommand(string command)
        {
            command = command.TrimEnd();
            return command += "\n";
        }

        public string ReadChannel()
        {
            string output = "";

            while(true)
            {
                if(this.shell_stream.DataAvailable)
                {
                    output += shell_stream.Read();
                }
                else
                {
                    break;
                }
            }
            return output;
        }

        public string ReadChannelUntil(string pattern="", int max_loops=100)
        {
            float loop_delay = 0.1f;
            string output = "";
            bool foundPattern = false;
            int sleep_delay = Convert.ToInt32(loop_delay * this.global_delay);

            Thread.Sleep(sleep_delay);

            if(String.IsNullOrEmpty(pattern))
            {
                pattern = this.base_prompt;
            }

            output += ReadChannel();

            for(int i = 0; i < max_loops; i++)
            {
                var regexMatch = Regex.Match(output, pattern);
                if(regexMatch.Success)
                {
                    foundPattern = true;
                    break;
                }
                output += ReadChannel();
                Thread.Sleep(sleep_delay);
            }

            if(!foundPattern)
            {
                throw new ApplicationException("Could not find pattern in data");
            }

            return output;
        }

        public void WriteChannel(string data)
        {
            shell_stream.Write(data);
        }
        public void Disconnect()
        {
            this.ssh_session.Disconnect();
            this.ssh_session.Dispose();
        }
    }
}
