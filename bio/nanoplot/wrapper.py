__author__ = "Kateřina Havlová"
__copyright__ = "Copyright 2026, Kateřina Havlová"
__email__ = "katkahemalova@gmail.com"
__license__ = "MIT"


from snakemake.shell import shell

extra = snakemake.params.get("extra", "")
log = snakemake.log_fmt_shell(stdout=True, stderr=True)

# NanoPlot's input options form a required, mutually exclusive argparse group,
# so exactly one may be given. Checking that here turns an argparse failure
# raised from inside a wrapper into a message naming the input keys.
SOURCES = (
    "fastq",
    "fastq_rich",
    "fastq_minimal",
    "fasta",
    "bam",
    "ubam",
    "cram",
    "summary",
    "pickle",
    "feather",
)
given = [s for s in SOURCES if snakemake.input.get(s)]
if len(given) != 1:
    raise ValueError(
        f"nanoplot needs exactly one input type from {', '.join(SOURCES)}; "
        f"got {given or 'none'}"
    )
source = given[0]
files = snakemake.input[source]

# NanoPlot fills a directory: the report, NanoStats.txt, an HTML and an image
# per plot, and a log. The plot set depends on the input type, so the output is
# declared as a directory rather than enumerated. The report embeds its figure
# data but loads plotly.js from a CDN, which makes the images the only offline
# view of the plots — reason enough to keep them rather than discard them.
shell(
    "NanoPlot"
    " --threads {snakemake.threads}"
    " --outdir {snakemake.output:q}"
    " --{source} {files:q}"
    " {extra}"
    " {log}"
)
