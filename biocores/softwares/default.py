#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2019-05-05 09:48
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : default.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
from collections import namedtuple

# fastp
fastpDefault = namedtuple('fastpDefault', ['default', 'pe', 'se'])
fastpDefault.default = ' -c  '
fastpDefault.pe = ' --detect_adapter_for_pe'
fastpDefault.se = ' '
# mkdir
mkdirDefault = namedtuple('mkdirDefault', ['default'])
mkdirDefault.default = ' -p '

# fastqc
fastqcDefault = namedtuple('fastqcDefault', ['default'])
fastqcDefault.default = ''

# star
starDefault = namedtuple('starDefault', ['align', 'mirna_align', 'build_index', 'nt', 'rl'])
starDefault.align = '--outSAMstrandField intronMotif --readFilesCommand zcat --outSAMtype BAM SortedByCoordinate'
starDefault.mirna_align = '--alignEndsType EndToEnd --outFilterMismatchNmax 1 ' \
                          '--outFilterMultimapScoreRange 0 --quantMode TranscriptomeSAM GeneCounts ' \
                          '--outReadsUnmapped Fastx  ' \
                          '--outFilterMultimapNmax 10 --outSAMunmapped Within ' \
                          '--outFilterScoreMinOverLread 0 --outFilterMatchNminOverLread 0 ' \
                          '--outFilterMatchNmin 16 --alignSJDBoverhangMin 1000 ' \
                          '--alignIntronMax 1 --outWigType wiggle --outWigStrand Stranded --outWigNorm RPM'
starDefault.build_index = ' --runMode genomeGenerate '
starDefault.nt = 8
starDefault.rl = 99

# hisat2
hisat2Default = namedtuple('hisat2Default', ['align', 'build_index', 'nt'])
hisat2Default.align = ' --dta -5 10 -3 10 '
hisat2Default.build_index = ''
hisat2Default.nt = ' 16 '

# samtools
samtoolsDefault = namedtuple('samtoolsDefault', ['sam2bam', 'sort', 'index'])
samtoolsDefault.sam2bam = ' view -bSt '
samtoolsDefault.sort = ' sort '
samtoolsDefault.index = ' index '

# stringtie
stringtieDefault = namedtuple('stringtieDefault', ['nt', 'merge'])
stringtieDefault.nt = 16
stringtieDefault.merge = '--merge -m 200 -F 0 -T 0 '

# trinity
trinityDefault = namedtuple('trinityDefault', ['default', 'nt', 'memory'])
trinityDefault.memory = '100G'
trinityDefault.nt = 16
trinityDefault.default = '--seqType fq --full_cleanup'

# java
JAVA_OPTIONS = '-Xmx30g -XX:+UseParallelGC -XX:ParallelGCThreads=2'

# picard
picardDefault = namedtuple('picardDefault', ['java_options',
                                             'markdup',
                                             'quality_score_distribution',
                                             'collect_gc_bias_metrics',
                                             'collect_wgs_metrics'])
picardDefault.java_options = JAVA_OPTIONS
picardDefault.markdup = ' MarkDuplicates ' \
                        'ASSUME_SORTED=true REMOVE_DUPLICATES=false VALIDATION_STRINGENCY=SILENT ' \
                        'MAX_RECORDS_IN_RAM=1750000 '
picardDefault.quality_score_distribution = ' QualityScoreDistribution '
picardDefault.collect_gc_bias_metrics = ' CollectGcBiasMetrics '
picardDefault.collect_wgs_metrics = ' CollectWgsMetrics '

# gffcompare
gffcompareDefault = namedtuple('gffcompareDefault', ['default'])
gffcompareDefault.default = ' -T '

# gffread
gffreadDefault = namedtuple('gffreadDefault', ['default'])
gffreadDefault.default = ''

# kallisto
kallistoDefault = namedtuple('kallistoDefault', ['index_paras', 'quant_paras', 'nt'])
kallistoDefault.index_paras = ' index '
kallistoDefault.quant_paras = ' quant --bias '
kallistoDefault.nt = 16

# minimap2
minimap2Default = namedtuple('minimap2Default', ['default', 'align_paras'])
minimap2Default.default = ' -I 10G '

# mirdeep2
mirdeep2Default = namedtuple('mirdeep2Default', ['default', 'align_paras', 'mirdeep2'])
mirdeep2Default.align_paras = ' -v -e -h -i -j -l 18 -m -o 4 '
mirdeep2Default.mirdeep2 = ''

# gatk4
gatk4Default = namedtuple('gatk4Default', ['java_options'])
gatk4Default.java_options = '"' + JAVA_OPTIONS + '"'

# bwa
bwaDefault = namedtuple('bwaDefault', ['mem', 'mirna_align', 'build_index'])
bwaDefault.build_index = ' index '
bwaDefault.mem = ' mem -t 10 -k 32 -M '
bwaDefault.mirna_align = ' aln -l 8 -o 0 '

# bowtie
bowtieDefault = namedtuple('bowtieDefault', ['align', 'mirna_align', 'build_index'])
bowtieDefault.build_index = '  '
bowtieDefault.mirna_align = ' -q -p 10 -k 100 --best --strata -S '

# bowtie2
bowtie2Default = namedtuple('bowtie2Default', ['align', 'mirna_align', 'build_index'])
bowtie2Default.build_index = '  '
bowtie2Default.mirna_align = ' -k 100 -q -p 20 --local --very-sensitive-local  '


# msisensor
msisensorDefault = namedtuple('msisensorDefault', ['msi'])
msisensorDefault.msi = ' -c 15 '

# cnvkit
cnvkitDefault = namedtuple('cnvkitDefault', ['batch', 'segment', 'germline_call', 'somatic_call'])
cnvkitDefault.batch = 'batch --drop-low-coverage --scatter --diagram '
cnvkitDefault.segment = 'segment '
cnvkitDefault.germline_call = ' call -t=-1.5,-0.6,0.6,1.3 '
cnvkitDefault.somatic_call = ' call -m clonal  -y '


# formattrans
formattransDefault = namedtuple('formattransDefault', ['default'])
formattransDefault.default = ''


# featurecounts
featurecountsDefault = namedtuple('featurecountsDefault', ['default'])
featurecountsDefault.default = ' -T 12 -p -t exon -g gene_id -M '

# OLD PARAMETERS=========================================================================
# bwa
BWA_MEM_DEFAULT = ' '
BWA_ALN_DEFAULT = ' aln -l 19'
BWA_SAMSE_DEFAULT = ' samse -n 10'

# gatk3.8
GATK_BASERECAL_DEFAULT = '-T BaseRecalibrator --downsampling_type None'
GATK_APPLY_BASERECAL_DEFAULT = '-T PrintReads'
GATK_HC_DEFAULT = '-T HaplotypeCaller --emitRefConfidence GVCF -dontUseSoftClippedBases --downsampling_type None ' \
                  '-stand_call_conf 30 --genotyping_mode DISCOVERY --min_base_quality_score 10 ' \
                  '--disable_auto_index_creation_and_locking_when_reading_rods ' \
                  '-variant_index_type LINEAR -variant_index_parameter 128000 '
GATK_SELECT_DEFAULT = '-T SelectVariants --disable_auto_index_creation_and_locking_when_reading_rods'
GATK_INDEL_FILTER_DEFAULT = '-T VariantFiltration ' \
                            '--filterExpression "QD < 2.0" --filterName "INDELflt_QD" ' \
                            '--filterExpression "ReadPosRankSum < -20.0" --filterName "INDELflt_RPRS" ' \
                            '--filterExpression "FS > 200.0" --filterName "INDELflt_FS" ' \
                            '--filterExpression "DP < 20" --filterName "INDELflt_DP" ' \
                            '--disable_auto_index_creation_and_locking_when_reading_rods'
GATK_SNP_FILTER_DEFAULT = '-T VariantFiltration ' \
                          '--filterExpression "QD < 2.0" --filterName "SNPflt_QD" ' \
                          '--filterExpression "MQ < 40.0" --filterName "SNPflt_MQ" ' \
                          '--filterExpression "ReadPosRankSum < -8.0" --filterName "SNPflt_RPRS" ' \
                          '--filterExpression "FS > 60.0" --filterName "SNPflt_FS" ' \
                          '--filterExpression "HaplotypeScore > 13.0" --filterName "SNPflt_HapS" ' \
                          '--filterExpression "MQRankSum < -12.5" --filterName "SNPflt_MQRS" ' \
                          '--filterExpression "DP < 20" --filterName "SNPflt_DP" ' \
                          '--clusterSize 3 --clusterWindowSize 10 ' \
                          '--disable_auto_index_creation_and_locking_when_reading_rods'
GATK_COMBINEVCF_DEFAULT = '-T CombineVariants --genotypemergeoption UNSORTED'
GATK_GENOTYPE_GVCF_DEFAULT = '-T GenotypeGVCFs '
GATK_INDEL_REALIGN_DEFAULT = '-T IndelRealigner '
GATK_VQSR_PRE_DEFAULT = '-T VariantRecalibrator '
GATK_VQSR_DEFAULT = '-T ApplyRecalibration --ts_filter_level 99.0 '
GATK_VQSR_PRE_SNP_AN = '-an QD -an MQ -an MQRankSum ' \
                       '-an ReadPosRankSum -an FS -an SOR -an DP'
GATK_VQSR_PRE_INDEL_AN = '-an QD -an DP -an FS -an SOR ' \
                         '-an ReadPosRankSum -an MQRankSum'
GATK_CONTEST_DEFAULT = '-T ContEst -isr INTERSECTION '
GATK_MUTECT2_DEFAULT = '-T MuTect2 -dt NONE -gt_mode DISCOVERY -dontUseSoftClippedBases '
# multiqc

MULTIQC_DEFAULT = '-f --title "Aegicare Bioinformatics Analysis" --data-format json ' \
                  '--zip-data-dir --interactive '

# cnvkit


# lumpy

SAMBLASTER_DEFAULT = '-M --excludeDups --addMateTags --maxSplitCount 2 --minNonOverlap 20 '

# sentieon
SENTIEON_NT_DEFAULT = '-t 16'
SENTIEON_BWA_MEM_DEFAULT = 'bwa mem -M -K 10000000 '
SENTIEON_SORT_DEFAULT = 'util sort --sam2bam '

# VEP

VEP_ANNOTATION_DEFAULT = '--format vcf --cache --offline --force_overwrite --sift b ' \
                         '--polyphen b --numbers --biotype --total_length --canonical --ccds --hgvs ' \
                         '-q --refseq --offline --vcf --af_1kg --af --pubmed --plugin MMSplice --af_gnomad '

# ANNOVAR

ANNOVAR_ANNOTATION_DEFAULT = '-remove -protocol refGene,cytoBand,exac03,ALL.sites.2015_08,EAS.sites.2015_08,' \
                             'esp6500siv2_all,regsnpintron,spidex,dbscsnv11,dbnsfp33a,clinPred,rmsk,intervar_20180118,' \
                             'gnomad_genome,clinvar_20190315,gnomad_20190215,hgmd_anno_201803,' \
                             'vcfposFreq_2019-02-19_het_hom,vcfposFreq_2019-02-19,aegicaredb_acmgDiseaseName,' \
                             'aegicaredb_diseaseGroup_level3,' \
                             'aegicaredb_diseaseOMIM,aegicaredb_HPO_describe_chinese_simple,aegicaredb_product_level1,' \
                             'aegicaredb_acmgDiseaseOMIM,aegicaredb_diseaseNameC,aegicaredb_geneOMIM,' \
                             'aegicaredb_HPO_describe_english_details,aegicaredb_product_level2,' \
                             'aegicaredb_diseaseGroup_level1,aegicaredb_diseaseNameE,aegicaredb_heritance,' \
                             'aegicaredb_HPO_describe_english_simple,aegicaredb_product_level3,' \
                             'aegicaredb_diseaseGroup_level2,aegicaredb_HPO_describe_chinese_details,' \
                             'aegicaredb_HPO,aegicaredb_transcript,revel_20190527 ' \
                             '-operation g,r,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,r,f ' \
                             '--otherinfo'

ANNOVAR_ANNOTATION_SIMPLE = '-remove -protocol refGene,cytoBand,exac03,ALL.sites.2015_08,EAS.sites.2015_08,' \
                            'esp6500siv2_all,regsnpintron,spidex,dbscsnv11,dbnsfp33a,clinPred,rmsk,' \
                            'intervar_20180118,gnomad_genome,gnomad_20190215,revel_20190527 ' \
                            '-operation g,r,f,f,f,f,f,f,f,f,f,f,f,f,f,f'

# TREDPARSE

TREDPARSE_DEFAULT = ' --cpus 4 --ref hg19_nochr '
TREDREPORT_DEFAULT = ' --cpus 4 --ref hg19_nochr '

# HIPSTR


# BCL2FASTQ2

BCL2FASTQ2_DEFAULT = '--create-fastq-for-index-reads --no-lane-splitting  ' \
                     '--with-failed-reads --ignore-missing-bcls ' \
                     '--ignore-missing-filter --ignore-missing-positions'

# MAIL RECEIVERS

MAIL_RECEIVERS_DEFAULT = 'yuelong.chen@aegicare.com hongli.hu@aegicare.com ' \
                         'miao.hou@aegicare.com yongchu.liu@aegicare.com huhongli@aegicare.cn'
