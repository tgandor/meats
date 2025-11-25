$pathogen = "$HOME\.vim\autoload\pathogen.vim"
$autoloadDir = "$HOME\.vim\autoload"
$bundleDir = "$HOME\.vim\bundle"
$vimrc = "$HOME\.vimrc"

# Create directories
New-Item -ItemType Directory -Force -Path $autoloadDir, $bundleDir | Out-Null

# Download pathogen.vim if it doesn't exist
if (Test-Path $pathogen) {
    Write-Host "$pathogen already present"
} else {
    Invoke-WebRequest -Uri "https://tpo.pe/pathogen.vim" -OutFile $pathogen
}

# Clone vim-renamer plugin if it doesn't exist
$pluginDir = Join-Path $bundleDir "vim-renamer"
if (Test-Path $pluginDir) {
    Write-Host "vim-renamer already in $bundleDir"
} else {
    git clone https://github.com/qpkorr/vim-renamer.git $pluginDir
}

if (!(Test-Path $vimrc)) {
    New-Item -ItemType File -Path $vimrc | Out-Null
}

# Add pathogen to .vimrc if it's not present
if (Select-String -Path $vimrc -Pattern "pathogen" -Quiet) {
    Write-Host "Pathogen already in .vimrc"
} else {
    Add-Content -Path $vimrc -Value "execute pathogen#infect()"
}
