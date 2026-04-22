% alcubierre_sanity.m
% ROADMAP Task 3.1 (Phase 4): standard Alcubierre EC reproduction.
% Pure tooling sanity check -- expects catastrophic NEC violation at
% the bubble wall, matching Pfenning-Ford 1997 / Helmerich et al. 2024 Fig. 6.
%
% Canonical Pfenning-Ford 1997 / textbook params:
%   v = 1 (c)        -- warp speed
%   R = 4 (m)        -- bubble radius
%   sigma = 8 (1/m)  -- wall sharpness
%
% Outputs (to pwd, copy to alcubierre/warp_factory_repro/):
%   alcubierre_textbook.mat   -- numeric data
%   alcubierre_textbook_*.png -- 4 EC maps + energy density

WF_ROOT = 'F:/science-projects/WarpFactory';
if ~isfolder(WF_ROOT)
    error('Warp Factory not found at %s.', WF_ROOT);
end
addpath(genpath(WF_ROOT));

%% Params
v = 1;
R = 4;
sigma = 8;

% Grid: cartoon-thin in z, dense in x/y
spaceScale = 5;
cartoonThickness = 5;
gridSize = ceil([1, 2*(R+4)*spaceScale, 2*(R+4)*spaceScale, cartoonThickness]);
gridScale = [1/(1000*c), 1/spaceScale, 1/spaceScale, 1/spaceScale];
worldCenter = [(1+1)/2, (gridSize(2)+1)/2, (gridSize(3)+1)/2, (cartoonThickness+1)/2] .* gridScale;

fprintf('=== Standard Alcubierre EC sanity (textbook params) ===\n');
fprintf('  v=%g c, R=%g m, sigma=%g 1/m\n', v, R, sigma);
fprintf('  grid: %dx%dx%dx%d, dx=%g m\n', gridSize(1), gridSize(2), gridSize(3), gridSize(4), 1/spaceScale);

%% Build + evaluate
t0 = tic;
Metric = metricGet_Alcubierre(gridSize, worldCenter, v, R, sigma, gridScale);
fprintf('  Metric build: %.1f s\n', toc(t0));

t0 = tic;
EC = evalMetric(Metric, 1, 1);
fprintf('  evalMetric:   %.1f s\n', toc(t0));

%% Extract mid-z slice
zIdx = round((cartoonThickness+1)/2);
nec = squeeze(EC.null    (1,3:end-2,3:end-2,zIdx))';
wec = squeeze(EC.weak    (1,3:end-2,3:end-2,zIdx))';
dec = squeeze(EC.dominant(1,3:end-2,3:end-2,zIdx))';
sec = squeeze(EC.strong  (1,3:end-2,3:end-2,zIdx))';

% xy coords for plotting
xc = ((3:gridSize(2)-2) - worldCenter(2)*spaceScale) / spaceScale;
yc = ((3:gridSize(3)-2) - worldCenter(3)*spaceScale) / spaceScale;
[Xg, Yg] = meshgrid(xc, yc);

%% Pass-fraction in a "bubble interior + wall" mask
r2grid = Xg.^2 + Yg.^2;
shellMask = r2grid <= (R + 2/sigma)^2;     % everything within bubble + 2 wall thicknesses
nMask = nnz(shellMask);
tol = -1e-12;
passNEC = sum(nec(shellMask) >= tol) / nMask;
passWEC = sum(wec(shellMask) >= tol) / nMask;
passDEC = sum(dec(shellMask) >= tol) / nMask;
passSEC = sum(sec(shellMask) >= tol) / nMask;

fprintf('\nPass fractions in bubble+wall mask:\n');
fprintf('  NEC = %.4f   (expect << 1: Alcubierre violates NEC at the wall)\n', passNEC);
fprintf('  WEC = %.4f\n', passWEC);
fprintf('  DEC = %.4f\n', passDEC);
fprintf('  SEC = %.4f\n', passSEC);
fprintf('\nExtremum diagnostics (within mask):\n');
fprintf('  min(NEC) = %+.3e\n', min(nec(shellMask)));
fprintf('  min(WEC) = %+.3e\n', min(wec(shellMask)));
fprintf('  min(DEC) = %+.3e\n', min(dec(shellMask)));
fprintf('  min(SEC) = %+.3e\n', min(sec(shellMask)));

%% Save raw
save('alcubierre_textbook.mat','EC','Metric','v','R','sigma','spaceScale', ...
    'gridSize','worldCenter','gridScale','xc','yc','Xg','Yg', ...
    'nec','wec','dec','sec','passNEC','passWEC','passDEC','passSEC','-v7');
fprintf('\nSaved alcubierre_textbook.mat\n');

%% Plots
plotEC = @(Z, name, fname) (function_handle_dummy());
% Inline plot helper (avoid separate file)
ecNames = {'NEC','WEC','DEC','SEC'};
ecData  = {nec, wec, dec, sec};
for i = 1:4
    fig = figure('Visible','off','Position',[100 100 600 500]);
    pcolor(Xg, Yg, ecData{i}); shading flat; axis equal tight;
    colormap(redblue_safe()); cb = colorbar; ylabel(cb, ecNames{i});
    % symmetric colour scale for sign visibility
    cmax = max(abs(ecData{i}(:)));
    if cmax > 0; caxis([-cmax cmax]); end
    hold on;
    th = linspace(0, 2*pi, 100);
    plot(R*cos(th), R*sin(th), 'k--', 'LineWidth', 1.5);
    xlabel('x [m]'); ylabel('y [m]');
    title(sprintf('Standard Alcubierre %s (v=%g c, R=%g, sigma=%g)', ecNames{i}, v, R, sigma));
    saveas(fig, sprintf('alcubierre_textbook_%s.png', lower(ecNames{i})));
    close(fig);
end
fprintf('Saved 4 EC plot PNGs.\n');

%% Energy density (T^00) plot if available
if isfield(EC, 'energyDensity')
    fig = figure('Visible','off','Position',[100 100 600 500]);
    rho = squeeze(EC.energyDensity(1,3:end-2,3:end-2,zIdx))';
    pcolor(Xg, Yg, rho); shading flat; axis equal tight;
    colormap(redblue_safe()); cb = colorbar; ylabel(cb, '\rho');
    cmax = max(abs(rho(:)));
    if cmax > 0; caxis([-cmax cmax]); end
    hold on; plot(R*cos(linspace(0,2*pi,100)), R*sin(linspace(0,2*pi,100)), 'k--', 'LineWidth', 1.5);
    xlabel('x [m]'); ylabel('y [m]');
    title(sprintf('Standard Alcubierre energy density (v=%g c)', v));
    saveas(fig, 'alcubierre_textbook_rho.png');
    close(fig);
    fprintf('Saved energy density plot.\n');
end

fprintf('\n=== DONE ===\n');

%% Helper -- redblue colormap safe even without imageprocessing toolbox
function cm = redblue_safe()
    n = 256;
    half = n/2;
    cm = zeros(n,3);
    cm(1:half,1)   = linspace(0, 1, half);
    cm(1:half,2)   = linspace(0, 1, half);
    cm(1:half,3)   = 1;
    cm(half+1:n,1) = 1;
    cm(half+1:n,2) = linspace(1, 0, half);
    cm(half+1:n,3) = linspace(1, 0, half);
end

function f = function_handle_dummy()
    f = @() [];
end
