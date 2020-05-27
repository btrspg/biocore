#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @License : Copyright(c) Aegicare License
# @Time    : 2020/3/1 10:53 AM
# @Author  : YUELONG.CHEN
# @Mail    : yuelong.chen.btr@gmail.com
# @File    : gatk4
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals

from biocores import utils
from biocores.bases.tasks import Task


class Gatk4(Task):
    def __init__(self, software, fd):
        super(Gatk4, self).__init__(software)
        self._default = fd

    def cmd_version(self):
        '''

        :return:
        '''
        return 'echo {repr} ; echo {software}'.format(
            repr=self.__repr__(),
            software=self._software
        )

    @utils.special_tmp
    @utils.modify_cmd
    def cmd_select_vcf(self, raw_vcf, snp_vcf, indel_vcf, reference, tmp):
        return r'''
{software} SelectVariants --tmp-dir {tmp} --java-options {java_options} \
    --disable_auto_index_creation_and_locking_when_reading_rods \
    -R {reference} \
    --variant {raw_vcf} \
    -o {snp_vcf} \
    -selectType SNP -selectType MNP
{software} SelectVariants --tmp-dir {tmp} --java-options {java_options} \
    --disable_auto_index_creation_and_locking_when_reading_rods \
    -R {reference} \
    --variant {raw_vcf} \
    -o {indel_vcf} \
    -selectType INDEL
        '''.format(
            software=self._software,
            tmp=tmp,
            reference=reference,
            raw_vcf=raw_vcf,
            snp_vcf=snp_vcf,
            indel_vcf=indel_vcf,
            java_options=self._default.java_options
        )

    @utils.modify_cmd
    @utils.special_tmp
    def cmd_create_pon(self, bams, intervals, af_file, reference, outdir, tmp):
        '''

        :param bams:
        :param intervals:
        :param af_file:
        :param reference:
        :param outdir:
        :param tmp:
        :return:
        '''
        mutect_call = []
        normal_vcfs = []
        for i, bam in enumerate(bams):
            mutect_call.append('{software} Mutect2 --tmp-dir {tmp} --java-options {java_options} '
                               '-R {reference} '
                               '-I {bam} --max-mnp-distance 0 '
                               '-O {outdir}/normal{i}.vcf.gz'.format(software=self._software,
                                                                     reference=reference,
                                                                     bam=bam,
                                                                     outdir=outdir,
                                                                     i=i,
                                                                     tmp=tmp,
                                                                     java_options=self._default.java_options))
            normal_vcfs.append('-V {outdir}/normal{i}.vcf.gz'.format(outdir=outdir, i=i))

        return r'''
{mutect_call}

{software} GenomicsDBImport --tmp-dir {tmp} --java-options {java_options} \
    -R {reference} \
    -L {intervals} \
    --genomicsdb-workspace-path {outdir}/pon.db \
    {vcfs}
  
{software} CreateSomaticPanelOfNormals --tmp-dir {tmp} --java-options {java_options} \
    -R {reference} \
    --germline-resource {af_file} \
    -V gendb://{outdir}/pon.db \
    -O {outdir}/pon.vcf.gz
        '''.format(
            mutect_call='\n'.join(mutect_call),
            software=self._software,
            tmp=tmp,
            java_options=self._default.java_options,
            reference=reference,
            intervals=intervals,
            af_file=af_file,
            outdir=outdir,
            vcfs=''.join(normal_vcfs)
        )

    @utils.special_tmp
    @utils.modify_cmd
    def cmd_base_recalibrator(self, bam_file, out_bam, reference, known_sites, qc_prefix, tmp='/tmp'):
        '''

        :param bam:
        :param out_bam:
        :param reference:
        :param known_sites:
        :param qc_prefix:
        :param tmp:
        :return:
        '''
        if isinstance(known_sites, str):
            known_sites = known_sites.split(',')
        if isinstance(known_sites, list):
            ks = ' '.join(['--known-sites {}'.format(i) for i in known_sites])
        else:
            raise TypeError('known-sites should be specific')
        return r'''
{software} BaseRecalibrator --tmp-dir {tmp} --java-options {java_options} \
   -I {bam_file} \
   -R {reference} \
   {ks} \
   -O {qc_prefix}.recal_data.table   
{software} ApplyBQSR --tmp-dir {tmp} --java-options {java_options} \
   -R {reference} \
   -I {bam_file} \
   --bqsr-recal-file {qc_prefix}.recal_data.table  \
   -O {out_bam}     
        '''.format(
            software=self._software,
            tmp=tmp,
            java_options=self._default.java_options,
            reference=reference,
            ks=ks,
            qc_prefix=qc_prefix,
            bam_file=bam_file,
            out_bam=out_bam
        )

    @utils.special_tmp
    @utils.modify_cmd
    def cmd_call_germline_mutation(self, bam_file, reference, target_interval, raw_vcf, tmp='/tmp'):
        '''

        :param bam_file:
        :param reference:
        :param target_interval:
        :param raw_vcf:
        :param tmp:
        :return:
        '''
        return r'''
{software} HaplotypeCaller --tmp-dir {tmp} --java-options {java_options} \
    -R {reference} \
    -I {bam_file} \
    -L {target_interval} \
    -O {raw_vcf} \
    -ERC GVCF -stand-call-conf 10      
        '''.format(
            software=self._software,
            reference=reference,
            tmp=tmp,
            target_interval=target_interval,
            raw_vcf=raw_vcf,
            bam_file=bam_file,
            java_options=self._default.java_options

        )

    @utils.special_tmp
    @utils.modify_cmd
    def cmd_genotype_vcf(self, in_vcf, reference, out_vcf, tmp):
        '''

        :param in_vcf:
        :param reference:
        :param out_vcf:
        :param tmp:
        :return:
        '''
        return r'''
{software} GenotypeGVCFs --tmp-dir {tmp} --java-options {java_options}  \
    -R {reference} \
    -V {in_vcf} \
    -O {out_vcf}     
        '''.format(
            software=self._software,
            tmp=tmp,
            java_options=self._default.java_options,
            in_vcf=in_vcf,
            out_vcf=out_vcf,
            reference=reference
        )

    @utils.special_tmp
    @utils.modify_cmd
    def cmd_call_somatic_mutation(self, t_id, n_id, t_bam, n_bam, reference, intervals, pon, gnomad,
                                  common, outdir, final_vcf, DP=50, AD=5, AF=0.05, tmp=utils.get_tempfile()):
        '''

        :param t_id:
        :param n_id:
        :param t_bam:
        :param n_bam:
        :param reference:
        :param intervals:
        :param pon:
        :param gnomad:
        :param common:
        :param outdir:
        :param final_vcf:
        :param DP:
        :param AD:
        :param AF:
        :param tmp:
        :return:
        '''

        control = ''
        gr = ''
        ponfile = ''

        if None is not n_id and None is not n_bam:
            control = ' -I ' + n_bam + ' -normal ' + n_id
        if None is not pon:
            ponfile = ' -pon ' + pon
        if None is not gnomad:
            gr = '-germline-resource ' + gnomad
        return r'''
{software} Mutect2 --tmp-dir {tmp} --java-options {java_options} \
    -I {t_bam} \
    {control} \
    -O {outdir}/{t_id}.unfiltered.vcf \
    -R {reference} \
    -L {intervals} \
    {ponfile} {gr} \
    --f1r2-tar-gz {outdir}/{t_id}.f1r2.tar.gz
    
{software} LearnReadOrientationModel --tmp-dir {tmp} --java-options {java_options} \
    -I {outdir}/{t_id}.f1r2.tar.gz \
    -O {outdir}/{t_id}.read-orientation-model.tar.gz

{software} GetPileupSummaries --tmp-dir {tmp} --java-options {java_options} \
    -I {t_bam} \
    -V {common} \
    -L {common} \
    -O {outdir}/{t_id}.getpileupsummaries.table
    
{software} CalculateContamination --tmp-dir {tmp} --java-options {java_options} \
    -I {outdir}/{t_id}.getpileupsummaries.table \
    -tumor-segmentation {outdir}/{t_id}.segments.table \
    -O {outdir}/{t_id}.contamination.table


{software} FilterMutectCalls --tmp-dir {tmp} --java-options {java_options} \
    -V {outdir}/{t_id}.unfiltered.vcf \
    --tumor-segmentation {outdir}/{t_id}.segments.table \
    --contamination-table {outdir}/{t_id}.contamination.table \
    --ob-priors {outdir}/{t_id}.read-orientation-model.tar.gz \
    -O {outdir}/{t_id}.unfiltered.somatic.vcf  \
    -R {reference}
    
{software} VariantFiltration --tmp-dir {tmp} --java-options {java_options} \
    -R {reference} \
    -V {outdir}/{t_id}.unfiltered.somatic.vcf \
    -O {outdir}/{t_id}.filtered.somatic.vcf \
    --filter-expression "DP < {DP}" \
    --filter-name "DPfiltered" \
    --filter-expression 'vc.getGenotype("{t_id}").getAD().0<{AD}' \
    --filter-name "ADfiltered"  
{software} SelectVariants --tmp-dir {tmp} --java-options {java_options} \
    --variant {outdir}/{t_id}.filtered.somatic.vcf \
    -select "vc.isNotFiltered()" \
    -O {final_vcf} \
    --sample-name {t_id}
        '''.format(
            software=self._software,
            outdir=outdir,
            t_id=t_id,
            reference=reference,
            common=common,
            control=control,
            gr=gr,
            final_vcf=final_vcf,
            ponfile=ponfile,
            intervals=intervals,
            t_bam=t_bam,
            tmp=tmp,
            java_options=self._default.java_options,
            DP=DP,
            AD=AD,
            AF=AF

        )

    def __repr__(self):
        return 'gatk:' + self._software

    def __str__(self):
        return 'Genome Analysis Toolkit'


def main():
    from biocores.softwares.default import gatk4Default
    bams = ['/agdisk/backup/clinic/AS10736/filtered.bam', '/agdisk/backup/clinic/AS10737/filtered.bam',
            '/agdisk/backup/clinic/AS10740/filtered.bam', '/agdisk/backup/clinic/AS10741/filtered.bam',
            '/agdisk/backup/clinic/AS10742/filtered.bam', '/agdisk/backup/clinic/AS10743/filtered.bam',
            '/agdisk/backup/clinic/AS10744/filtered.bam', '/agdisk/backup/clinic/AS10745/filtered.bam',
            '/agdisk/backup/clinic/AS10746/filtered.bam', '/agdisk/backup/clinic/AS10747/filtered.bam',
            '/agdisk/backup/clinic/AS10748/filtered.bam', '/agdisk/backup/clinic/AS10749/filtered.bam',
            '/agdisk/backup/clinic/AS10787/filtered.bam', '/agdisk/backup/clinic/AS10788/filtered.bam',
            '/agdisk/backup/clinic/AS10789/filtered.bam', '/agdisk/backup/clinic/AS10790/filtered.bam',
            '/agdisk/backup/clinic/AS10791/filtered.bam', '/agdisk/backup/clinic/AS10792/filtered.bam',
            '/agdisk/backup/clinic/AS10793/filtered.bam', '/agdisk/backup/clinic/AS10794/filtered.bam',
            '/agdisk/backup/clinic/AS10795/filtered.bam', '/agdisk/backup/clinic/AS10796/filtered.bam',
            '/agdisk/backup/clinic/AS10800/filtered.bam', '/agdisk/backup/clinic/AS10801/filtered.bam',
            '/agdisk/backup/clinic/AS10804/filtered.bam', '/agdisk/backup/clinic/AS10805/filtered.bam',
            '/agdisk/backup/clinic/AS10806/filtered.bam', '/agdisk/backup/clinic/AS10808/filtered.bam',
            '/agdisk/backup/clinic/AS10811/filtered.bam', '/agdisk/backup/clinic/AS10812/filtered.bam',
            '/agdisk/backup/clinic/AS10815/filtered.bam', '/agdisk/backup/clinic/AS10816/filtered.bam',
            '/agdisk/backup/clinic/AS10817/filtered.bam', '/agdisk/backup/clinic/AS10820/filtered.bam',
            '/agdisk/backup/clinic/AS10821/filtered.bam', '/agdisk/backup/clinic/AS10822/filtered.bam',
            '/agdisk/backup/clinic/AS10823/filtered.bam', '/agdisk/backup/clinic/AS10824/filtered.bam',
            '/agdisk/backup/clinic/AS10825/filtered.bam', '/agdisk/backup/clinic/AS10826/filtered.bam',
            '/agdisk/backup/clinic/AS10827/filtered.bam', '/agdisk/backup/clinic/AS10831/filtered.bam',
            '/agdisk/backup/clinic/AS10832/filtered.bam', '/agdisk/backup/clinic/AS10835/filtered.bam',
            '/agdisk/backup/clinic/AS10838/filtered.bam', '/agdisk/backup/clinic/AS10839/filtered.bam',
            '/agdisk/backup/clinic/AS10840/filtered.bam', '/agdisk/backup/clinic/AS10841/filtered.bam',
            '/agdisk/backup/clinic/AS10842/filtered.bam', '/agdisk/backup/clinic/AS10844/filtered.bam',
            '/agdisk/backup/clinic/AS10851/filtered.bam', '/agdisk/backup/clinic/AS10852/filtered.bam',
            '/agdisk/backup/clinic/AS10856/filtered.bam', '/agdisk/backup/clinic/AS10862/filtered.bam',
            '/agdisk/backup/clinic/AS10863/filtered.bam', '/agdisk/backup/clinic/AS10864/filtered.bam',
            '/agdisk/backup/clinic/AS10866/filtered.bam', '/agdisk/backup/clinic/AS10871/filtered.bam',
            '/agdisk/backup/clinic/AS10874/filtered.bam', '/agdisk/backup/clinic/AS10880/filtered.bam',
            '/agdisk/backup/clinic/AS10881/filtered.bam', '/agdisk/backup/clinic/AS10882/filtered.bam',
            '/agdisk/backup/clinic/AS10883/filtered.bam', '/agdisk/backup/clinic/AS10884/filtered.bam',
            '/agdisk/backup/clinic/AS10885/filtered.bam', '/agdisk/backup/clinic/AS10891/filtered.bam',
            '/agdisk/backup/clinic/AS10894/filtered.bam', '/agdisk/backup/clinic/AS10895/filtered.bam',
            '/agdisk/backup/clinic/AS10901/filtered.bam', '/agdisk/backup/clinic/AS10902/filtered.bam',
            '/agdisk/backup/clinic/AS10910/filtered.bam', '/agdisk/backup/clinic/AS10911/filtered.bam',
            '/agdisk/backup/clinic/AS10912/filtered.bam', '/agdisk/backup/clinic/AS10913/filtered.bam',
            '/agdisk/backup/clinic/AS10914/filtered.bam', '/agdisk/backup/clinic/AS10915/filtered.bam',
            '/agdisk/backup/clinic/AS10916/filtered.bam', '/agdisk/backup/clinic/AS10917/filtered.bam',
            '/agdisk/backup/clinic/AS10918/filtered.bam', '/agdisk/backup/clinic/AS10921/filtered.bam',
            '/agdisk/backup/clinic/AS10922/filtered.bam', '/agdisk/backup/clinic/AS10924/filtered.bam',
            '/agdisk/backup/clinic/AS10933/filtered.bam', '/agdisk/backup/clinic/AS10934/filtered.bam',
            '/agdisk/backup/clinic/AS10935/filtered.bam', '/agdisk/backup/clinic/AS10936/filtered.bam',
            '/agdisk/backup/clinic/AS10937/filtered.bam', '/agdisk/backup/clinic/AS10938/filtered.bam',
            '/agdisk/backup/clinic/AS10939/filtered.bam', '/agdisk/backup/clinic/AS10940/filtered.bam',
            '/agdisk/backup/clinic/AS10941/filtered.bam', '/agdisk/backup/clinic/AS10942/filtered.bam',
            '/agdisk/backup/clinic/AS10943/filtered.bam', '/agdisk/backup/clinic/AS10944/filtered.bam']
    gatk=Gatk4('gatk4',gatk4Default)
    print(gatk.cmd_create_pon(bams,'/aegis/database/human/hg19/enrichments/wes/idt/xgen-exome-research-panel-targets.v0.intervals',
                        '/aegis/database/human/hg19/annotations/hapmap_3.3_hg19_2nochr_pop_stratified_af.vcf',
                        '/aegis/database/human/hg19/aegicare-pipe-database/references/genomes/human_g1k_v37/sequences/v1/human_g1k_v37_modified.fasta',
                        '/aegis/temp/pon/pon_idt',
                        '/aegis/temp/tmp'))

if __name__ == '__main__':
    main()