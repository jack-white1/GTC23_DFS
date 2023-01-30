%fftbeforedered = table2array(fftbeforedered);
%fftafterdered = table2array(fftafterdered);

tiledlayout(2,2);
nexttile;
histogram(fftbeforedered(:,1));
title('Before dereddening, real component');
text(-60000000,16000,num2str(std(fftbeforedered(:,1))));

nexttile;
histogram(fftbeforedered(:,2));
title('Before dereddening, imaginary component');
text(-60000000,16000,num2str(std(fftbeforedered(:,2))));


nexttile;
histogram(fftafterdered(:,1));
title('After dereddening, real component');
text(-3,16000,num2str(std(fftafterdered(:,1))));

nexttile;
histogram(fftafterdered(:,2));
title('After dereddening, imaginary component');
text(-3,16000,num2str(std(fftafterdered(:,2))));
