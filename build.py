import os

base_address = 0x80400000
step = 0x20000
linker = "src/linker.ld"

app_id = 0
apps = os.listdir("build/app")
apps.sort()
chapter = os.getenv("CHAPTER")
mode = os.getenv("MODE", default = "release")
if mode == "release" :
	mode_arg = "--release"
else :
    mode_arg = ""

for app in apps:
    app = app[: app.find(".")]
    #
    os.system(
        # generate object files by compiling source codes.
        #
        # cargo rustc --bin hello_world --release -- Clink-args=Ttext=0x80400000
        #
        #       --bin [<NAME>]      Build only the specified binary
        #       --release           Use release mode, which enables -O3 optimization, etc.
        #       --                  Separator indicating the subsequent parameters are passed to `rustc`
        #       -C, --codegen <OPT>[=<VALUE>] Set a codegen option
        #
        #           link-args specifies that it's an argument for linker.
        #           -Ttext=0x80400000 T=template, text=.text section. It explicitly specifies the load address of the code.
        "cargo rustc --bin %s %s -- -Clink-args=-Ttext=%x"
        % (app, mode_arg, base_address + step * app_id)
    )
    print(
        "[build.py] application %s start with address %s"
        % (app, hex(base_address + step * app_id))
    )
    if chapter == '3':
        app_id = app_id + 1
