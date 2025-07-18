{ pkgs, ... }: {
  channel = "stable-24.05";

  packages = [
    pkgs.python310Full
    pkgs.git
    pkgs.direnv
  ];

  env = {
    VIRTUAL_ENV = ".venv";
  };

  idx = {
    extensions = [ ];

    previews = {
      enable = true;
      previews = { };
    };

    workspace = {
      onCreate = {
        create-venv = "python3 -m venv .venv";
      };
      onStart = {
        activate-venv = "source .venv/bin/activate";
      };
    };
  };
}
