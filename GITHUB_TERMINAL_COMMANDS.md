cd ~/Downloads/BuildingWaterTankHygieneMonitor_WaterTankCare_Local
git init
git branch -M main
git add -A
git commit -m "feat: add WaterTankCare building water-tank hygiene monitor"
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/shaunakmirajgaonkar/building-water-tank-hygiene-monitor.git
git push -u origin main
