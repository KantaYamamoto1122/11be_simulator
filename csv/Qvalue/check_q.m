
clear all
name="Qvalue_n1.csv";
n0_q = readmatrix(name);

cw = [4 8 16 32 64 128 256];
sz = size(cw);
row = 2:1:sz(2)+1;
plot(n0_q(:,1),n0_q(:,row+1),'LineWidth',1.0)
axis square
set( gca, 'FontName','Times','FontSize',20);    
ax=gca;
ax.LineWidth = 1.5;
ax.Color = 'none';  
xlabel( 'Time({\it \mu}sec)', 'FontName','Times','FontSize',22 );   %
ylabel( 'Q value', 'FontName','Times','FontSize',22 );
cw_list = string(cw);
legend(cw_list)