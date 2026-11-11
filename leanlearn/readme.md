Please edit this document if you find the steps wrong. Instructions to install lean and get started with mechanics of proof.

book [link](https://hrmacbeth.github.io/math2001/index.html)


1) open vscode and do the [guide](https://lean-lang.org/install/). I could not get step 3 working without cloning the repo
2) git clone https://github.com/hrmacbeth/math2001.git
3) cd math2001
4) lake build (run into issue see step 5 below)


If you want to make your own project you can do the following:
1) lake new MyLeanProject
2) cd MyLeanProject
3) edit lakefile.toml to include the following: 
[[require]]
name = "mathlib"
scope = "leanprover-community"
4) lake build
5) curl -L https://raw.githubusercontent.com/leanprover-community/mathlib4/master/lean-toolchain -o lean-toolchain
6) lake update
7) lake exe cache get

