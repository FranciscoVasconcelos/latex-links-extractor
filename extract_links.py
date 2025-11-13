
# import re
import regex as re

base_url = "https://raw.githubusercontent.com/FranciscoVasconcelos/AppendixCFMCRCGA/refs/heads/main/Appendix.pdf"

# base_url = "https://github.com/FranciscoVasconcelos/AppendixCFMCRCGA/blob/main/Appendix.pdf?raw=true"


# pattern = re.compile(
#     r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}\{([^}]*)\}.*\{([^}]*)\}"
# )
rx = re.compile(r'\{(?:[^{}]+|(?R))+\}')

# aux_files = ["output.aux","appendix.aux"]
aux_files = ["output.aux"]

with open("appendix_links.tex", "w") as out:
    out.write("\\makeatletter\n")
    out.write("\\newcommand{\\linkref}[1]{\\csname #1@link\\endcsname}\n")
    out.write("\\newcommand{\\labelref}[1]{\\csname #1@label\\endcsname}\n")
    out.write("\\newcommand{\\pagewref}[1]{\\csname #1@page\\endcsname}\n")
    out.write("\\newcommand{\\refweb}[1]{\\href{\\linkref{#1}}{\\labelref{#1}}}\n")
    out.write("\n")

    for file in aux_files:
        with open(file) as f:
           
            for line in f:
                # m = pattern.match(line.strip()).group(0)
                if "newlabel" not in line:
                    continue
                
                parts = []
                for match in rx.finditer(line):
                    parts += [match.group(0)[1:-1]]

                label = parts[0] 
                number = parts[1] # The equation number
                page = parts[2] # The page number
                dest = parts[-1]
                url = f"{base_url}\\#{dest}"

                out.write(
                     f"\\expandafter\\newcommand\\csname {label}@link\\endcsname{{{url}}}\n"
                )
                
                out.write(
                     f"\\expandafter\\newcommand\\csname {label}@label\\endcsname{{{number}}}\n"
                )
                out.write(
                     f"\\expandafter\\newcommand\\csname {label}@page\\endcsname{{{page}}}\n\n"
                )


    out.write("\\makeatother\n")





