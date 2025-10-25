import os
import subprocess
import winreg
import psutil
import json

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)



def is_windows_11():
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") as k:
            product, _ = winreg.QueryValueEx(k, "ProductName")
            if product and "windows 11" in product.lower():
                return True
            try:
                build, _ = winreg.QueryValueEx(k, "CurrentBuild")
            except OSError:
                build, _ = winreg.QueryValueEx(k, "CurrentBuildNumber")
            build = int(build)
            return build >= 22000
    except Exception:
        return False


def GetSkins():
    Win11 = is_windows_11()

    if(not Win11):

        cmd = r"""$wmicOutput = wmic PROCESS WHERE name=`'LeagueClientUx.exe`' GET commandline
        $port = ($wmicOutput  | Select-String -Pattern '--app-port=([0-9]*)').matches.groups[1].Value
        $token = ($wmicOutput | Select-String -Pattern '--remoting-auth-token=([\w-]*)').matches.groups[1].Value

        $summonerId = (curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-summoner/v1/current-summoner | ConvertFrom-json).summonerId

        $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
        curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-champions/v1/inventories/$summonerId/skins-minimal > skins.json
        curl.exe --insecure -H "Accept: application/json" -u riot:$token https://127.0.0.1:$port/lol-loot/v1/player-loot > skinsLoot.json"""

    if (Win11):
        cmd = r"""
        $proc = Get-CimInstance Win32_Process -Filter "Name='LeagueClientUx.exe'" -ErrorAction SilentlyContinue
        $cmd = $proc.CommandLine
        if (-not $cmd) {
        Write-Error "Keine CommandLine verfügbar."
        return
        }


        if ($cmd -match '--app-port=(\d+)') { $port = $Matches[1] } else { Write-Error "app-port nicht gefunden."; return }
        if ($cmd -match '--remoting-auth-token=([\w-]+)') { $token = $Matches[1] } else { Write-Error "remoting-auth-token nicht gefunden."; return }

        $test = Test-NetConnection -ComputerName '127.0.0.1' -Port $port -WarningAction SilentlyContinue
        if (-not $test.TcpTestSucceeded) {
        Write-Error "127.0.0.1:$port nicht erreichbar. Firewall/Antivirus oder Client nicht wie erwartet."
        return
        }


        $curlPath = Join-Path $env:windir "System32\curl.exe"
        if (-not (Test-Path $curlPath)) { $curlPath = "curl.exe" }

        $summonerJson = & $curlPath --insecure -H "Accept: application/json" -u "riot:$token" "https://127.0.0.1:$port/lol-summoner/v1/current-summoner" 2>$null
        if (-not $summonerJson) { Write-Error "Konnte summoner endpoint nicht erreichen oder leere Antwort."; return }
        try {
        $summoner = $summonerJson | ConvertFrom-Json
        $summonerId = $summoner.summonerId
        } catch {
        Write-Error "Fehler beim Parsen der Summoner-Antwort."
        return
        }
        $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
        & $curlPath --insecure -H "Accept: application/json" -u "riot:$token" "https://127.0.0.1:$port/lol-champions/v1/inventories/$summonerId/skins-minimal" > skins.json
        & $curlPath --insecure -H "Accept: application/json" -u "riot:$token" "https://127.0.0.1:$port/lol-loot/v1/player-loot" > skinsLoot.json
        """

    subprocess.run (["powershell", "-Command", cmd], capture_output=True, text=True)


def CleanData():

    cleanData = []
    with open("skins.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    for item in data:
        cleanData.append({"championId": item["championId"], "name": item["name"], "owned": item["ownership"]["owned"], "tilePath": item["tilePath"]})
    
    with open("cleanedData.json", "w", encoding="utf-8-sig") as f:
        json.dump(cleanData, f)



if __name__ == "__main__":


    is_running = any(p.name().lower() == "leagueclientux.exe" for p in psutil.process_iter())


    if is_windows_11():
        print("You are running Win11")
    else:
        print("Running Win10 or older")

    if is_running:
        GetSkins()
        CleanData()
    else:
        print("LeagueClientUx.exe nicht gefunden")