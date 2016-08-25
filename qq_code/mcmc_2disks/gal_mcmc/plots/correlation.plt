reset 


set xlabel "r (kpc)" font ", 26" 
set ylabel "{/Symbol x}(r)" font ", 26" offset -1,0
set xtics font ", 22"
set ytics font ", 22"

set xrange[0.005:2]
set yrange[-1:2]


set term postscript enhanced color portrait
set size square

set nokey

set log x

set output "./correlation.ps"

plot    "../../data/correlation_0.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_1.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_2.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_3.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_4.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_5.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_6.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_7.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_8.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_9.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_10.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_11.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_12.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_13.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_14.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_15.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_16.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_17.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_18.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_19.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_20.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_21.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_22.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_23.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_24.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_25.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_26.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_27.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_28.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_29.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_30.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_31.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_32.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_34.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_35.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_36.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_37.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_38.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_39.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_40.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_41.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_42.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_43.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_44.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_45.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_46.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_47.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_48.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_49.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_50.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_51.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_52.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_53.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_54.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_55.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_56.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_57.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_58.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_59.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_60.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_61.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_63.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_64.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_65.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_66.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_67.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_68.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_69.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_70.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_71.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_72.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_73.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_74.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_75.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_76.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_77.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_78.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_79.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_81.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_82.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_83.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_84.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_85.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_86.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_87.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_88.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_89.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_90.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_91.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_92.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_93.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_95.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_97.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_98.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_99.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_100.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_101.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_102.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_103.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_104.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_105.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_106.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_107.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_108.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_109.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_110.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_111.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_112.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_114.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_115.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_116.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_117.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_118.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_120.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_121.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_122.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_123.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_124.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_125.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_129.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_130.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_131.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_133.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_134.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_135.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_136.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_137.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_138.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_139.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_140.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_141.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_142.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_143.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_144.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_145.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_146.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_147.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_148.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_149.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_150.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_151.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_152.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_153.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_154.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_155.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_156.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_157.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_158.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_159.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_160.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_161.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	"../../data/correlation_163.dat" u 3:6 w l lt 1 lw 0.1 lc rgb "gray", \
	0 with line lt 0 lw 2, \
	"../data/correlation.dat" u 3:6:15 w yerrorbars pt 7 ps 1.3 lt 1 lw 3 lc rgb "blue"	


#"../data/correlation.dat" u 3:6:14 w yerrorbars pt 7 ps 1.3 lt 1 lw 3 lc rgb "red", \
