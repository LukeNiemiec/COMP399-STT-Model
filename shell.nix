{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python312;

  runtimeLibs = with pkgs; [
    stdenv.cc.cc.lib
    zlib
    glib
    openssl
    libffi
    libsndfile
    ffmpeg
  ];
in
pkgs.mkShell {
  packages = with pkgs; [
    python
    git
    pkg-config
    gcc
    gnumake
    cmake
  ] ++ runtimeLibs;

  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath runtimeLibs;

  shellHook = ''
    export OMP_NUM_THREADS=4
    export TOKENIZERS_PARALLELISM=false
    export PYTHONUNBUFFERED=1

    if [ ! -d .venv ]; then
      python -m venv .venv
    fi

    source .venv/bin/activate

    echo "NeMo ASR development environment"
    python --version
    echo "Virtual environment: $VIRTUAL_ENV"

	# INITIAL SETUP 
    # python -m pip install --upgrade pip setuptools wheel
    
    # python -m pip install torch \
      # --index-url https://download.pytorch.org/whl/cpu
    
    # python -m pip install "nemo-toolkit[asr]"
  '';
}
