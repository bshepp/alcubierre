% fuchs_fig10_repro.m
% Headless reproduction of Fuchs et al. 2024 (arXiv:2405.02709) Fig. 10
% via Warp Factory (Helmerich et al. 2024, arXiv:2404.03095).
%
% Anchors TRUST_AUDIT #3 / ROADMAP 2A.9b (Alcubierre repo).
%
% Outputs (in CWD):
%   fuchs_repro.mat      -- numeric data (metric, energy tensor, NEC/WEC/DEC/SEC arrays)
%   fuchs_repro_*.png    -- energy-density + 4 energy-condition maps

addpath(genpath(pwd));

%% Canonical Fuchs parameters (W1_Warp_Shell.mlx defaults)
spaceScale = 5;
timeScale = 1;
centered = 1;
cartoonThickness = 5;
R1 = 10;
Rbuff = 0;
R2 = 20;
factor = 1/3;
m = R2/(2*G)*c^2*factor;            % ~4.49e27 kg
vWarp = 0.02;
sigma = 0;
doWarp = 1;
smoothFactor = 4000;

if centered == 1
    gridSize = ceil([1,2*(R2+10)*spaceScale,2*(R2+10)*spaceScale,cartoonThickness]);
else
    gridSize = ceil([1,(R2+10)*spaceScale,(R2+10)*spaceScale,cartoonThickness]);
end

gridScaling = [1/(timeScale*spaceScale*((vWarp)*c+1)),1/spaceScale,1/spaceScale,1/spaceScale];
gridScaling(1) = 1/(1000*c);
if centered == 1
    worldCenter = [(cartoonThickness+1)/2,(2*(R2+10)*spaceScale+1)/2,(2*(R2+10)*spaceScale+1)/2,(cartoonThickness+1)/2].*gridScaling;
else
    worldCenter = [(cartoonThickness+1)/2,5,5,(cartoonThickness+1)/2].*gridScaling;
end

if centered == 1
    x = linspace(0,2*(R2+10),gridSize(2)-4)';
    y = linspace(0,2*(R2+10),gridSize(3)-4)';
else
    x = linspace(0,(R2+10),gridSize(2)-4)';
    y = linspace(0,(R2+10),gridSize(3)-4)';
end
[X,Y] = meshgrid(x,y);

fprintf('[%s] Building Fuchs warp-shell metric: R1=%g, R2=%g, m=%.3e kg, vWarp=%g, gridSize=[%s]\n', ...
    datestr(now,'HH:MM:SS'), R1, R2, m, vWarp, num2str(gridSize));
t0 = tic;
Metric = metricGet_WarpShellComoving(gridSize,worldCenter,m,R1,R2,Rbuff,sigma,smoothFactor,vWarp,doWarp,gridScaling);
fprintf('[%s] Metric built in %.1f s\n', datestr(now,'HH:MM:SS'), toc(t0));

fprintf('[%s] Evaluating energy tensor + energy conditions ...\n', datestr(now,'HH:MM:SS'));
t1 = tic;
EC = evalMetric(Metric,1,1);
fprintf('[%s] evalMetric done in %.1f s\n', datestr(now,'HH:MM:SS'), toc(t1));

%% Mid-z slice
zOffset = 0;
zIdx = round((cartoonThickness+1)/2 + zOffset);

% Energy density
rho = squeeze(EC.energyTensorEulerian.tensor{1,1}(1,3:end-2,3:end-2,zIdx))';

% Energy conditions
nec = squeeze(EC.null   (1,3:end-2,3:end-2,zIdx))';
wec = squeeze(EC.weak   (1,3:end-2,3:end-2,zIdx))';
dec = squeeze(EC.dominant(1,3:end-2,3:end-2,zIdx))';
sec = squeeze(EC.strong (1,3:end-2,3:end-2,zIdx))';

%% Save numeric outputs
save('fuchs_repro.mat', ...
    'R1','R2','Rbuff','m','vWarp','sigma','smoothFactor','spaceScale','cartoonThickness', ...
    'X','Y','rho','nec','wec','dec','sec','-v7');

%% Pass-fraction summary (within shell mask R1<=r<=R2)
xc = X - mean(x);  yc = Y - mean(y);
r2 = xc.^2 + yc.^2;
shellMask = (r2 >= R1^2) & (r2 <= R2^2);

passNEC = sum(nec(shellMask) >= -1e-12) / nnz(shellMask);
passWEC = sum(wec(shellMask) >= -1e-12) / nnz(shellMask);
passDEC = sum(dec(shellMask) >= -1e-12) / nnz(shellMask);
passSEC = sum(sec(shellMask) >= -1e-12) / nnz(shellMask);

fprintf('\n=== PASS FRACTIONS (in-shell, R1<=r<=R2) ===\n');
fprintf('NEC: %.4f   WEC: %.4f   DEC: %.4f   SEC: %.4f\n', passNEC,passWEC,passDEC,passSEC);
fprintf('=== EXPECTED (Fuchs Fig 10): NEC, WEC, DEC -> 1.0; SEC may fail ===\n\n');

%% Headless plotting
mkpng = @(name) print('-dpng','-r150', name);

f = figure('Visible','off','Position',[100,100,800,700]);
imagesc(x,y,rho); axis equal tight; colorbar; colormap(flipud(redblue(rho)));
title(sprintf('Energy density (Eulerian),  passNEC=%.3f passWEC=%.3f passDEC=%.3f', ...
    passNEC,passWEC,passDEC));
xlabel('X [m]'); ylabel('Y [m]'); set(gca,'YDir','normal');
mkpng('fuchs_repro_rho.png'); close(f);

names = {'NEC','WEC','DEC','SEC'};
arrs  = {nec, wec, dec, sec};
passF = [passNEC, passWEC, passDEC, passSEC];
for k = 1:4
    f = figure('Visible','off','Position',[100,100,800,700]);
    A = arrs{k};
    imagesc(x,y,A); axis equal tight; colorbar; colormap(redblue(A));
    title(sprintf('%s   pass-fraction (in-shell) = %.4f', names{k}, passF(k)));
    xlabel('X [m]'); ylabel('Y [m]'); set(gca,'YDir','normal');
    hold on;
    th = linspace(0,2*pi,200);
    plot(mean(x)+R1*cos(th), mean(y)+R1*sin(th), 'k--');
    plot(mean(x)+R2*cos(th), mean(y)+R2*sin(th), 'k-');
    hold off;
    mkpng(sprintf('fuchs_repro_%s.png', lower(names{k}))); close(f);
end

fprintf('Outputs written: fuchs_repro.mat + 5 PNGs in %s\n', pwd);
