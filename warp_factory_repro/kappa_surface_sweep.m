% kappa_surface_sweep.m
% ROADMAP Task 3.2 (Phase 3 numerical verification):
%   Test whether kappa in Delta_min/R2 = kappa * beta / C is universal
%   or just a slice value of Session 18's anchor (M_canon, R2=20, beta=0.02).
%
% Outer grid: 3 (M) x 3 (R2) x 3 (beta) = 27 cells.
% Inner per cell: 6 Delta candidates spanning kappa in [1.5, 15].
% Total: 162 metric builds. Expected wallclock: ~80 min headless.
%
% Self-check anchor: (M_canon, R2=20, beta=0.02) must recover Session 18's
% kappa in (4.17, 5.83] within +/- 1 Delta-grid step. If this fails the
% rest of the sweep is suspect.
%
% Outputs (to pwd, copy to alcubierre/warp_factory_repro/ after run):
%   kappa_surface_sweep.mat -- full results array
%   kappa_surface_sweep.csv -- flat table for plotting
%   kappa_surface_*.png     -- diagnostic plots

% Resolve Warp Factory root (out-of-tree dependency).
WF_ROOT = 'F:/science-projects/WarpFactory';
if ~isfolder(WF_ROOT)
    error('Warp Factory not found at %s. Edit WF_ROOT at top of script.', WF_ROOT);
end
addpath(genpath(WF_ROOT));
addpath(genpath(pwd));

%% Outer grid -- (M, R2, beta)
%   M parameterised through factor C = 2GM/(R2 c^2); factor in {1/6, 1/3, 1/2}.
%   This brackets Session 18 (factor=1/3) by 2x in either direction while
%   staying clear of the Schwarzschild limit (factor < 2/3).
factors = [1/6, 1/3, 1/2];          % C compactness (3)
R2s     = [15, 20, 30];             % outer radius [m] (3)
betas   = [0.005, 0.02, 0.05];      % v_warp/c (3)

% Resolution discipline: keep spaceScale*R2 ~ 100 across the sweep.
%   R2=15  -> spaceScale=7  -> 105 in-shell radial pts
%   R2=20  -> spaceScale=5  -> 100 in-shell radial pts
%   R2=30  -> spaceScale=4  -> 120 in-shell radial pts
%   total grid points ~constant: 2*(R2+10)*spaceScale in {350, 300, 320}
spaceScaleMap = containers.Map({15, 20, 30}, {7, 5, 4});

% Inner Delta grid (per cell): kappa_grid * beta / C * R2.
%   kappa_grid covers [1.5, 15] which brackets Session 18's (4.17, 5.83].
kappa_grid = [1.5, 3.0, 5.0, 7.0, 10.0, 15.0];
nK = numel(kappa_grid);

%% Fixed Fuchs params
timeScale = 1;
centered = 1;
cartoonThickness = 5;
Rbuff = 0;
sigma = 0;
doWarp = 1;
smoothFactor = 4000;
tol = -1e-12;

%% Anchor self-check first
fprintf('=== ANCHOR SELF-CHECK (M_canon, R2=20, beta=0.02) ===\n');
fprintf('Expected Session 18 result: DEC transitions in Delta in (4.17, 5.83]\n');
fprintf('  -> kappa in (%.3f, %.3f]\n', 4.17*(1/3)/(0.02*20), 5.83*(1/3)/(0.02*20));
fprintf('  -> kappa in (4.17, 5.83] (since C/(beta*R2) = (1/3)/(0.02*20) = 0.833... wait)\n');
% Recompute: kappa = Delta * C / (beta * R2). With Delta=5, C=1/3, beta=0.02, R2=20:
%   kappa = 5 * (1/3) / (0.02*20) = 5/12 = 0.417. That doesn't match either.
% Session 18 reported kappa in (4.17, 5.83]. So convention there must have been
%   kappa = Delta / (beta * R2 / C) = Delta * C / (beta * R2)... let's just compute
%   what we get and document it.

%% Loop
nC = numel(factors); nR = numel(R2s); nB = numel(betas);
nCells = nC*nR*nB;
results = struct( ...
    'factor',{},'C',{},'R2',{},'beta',{},'m',{}, ...
    'Deltas',{},'kappas_grid',{},'passDEC',{},'passNEC',{},'passWEC',{},'passSEC',{}, ...
    'minDEC_inshell',{},'spaceScale',{},'gridSize',{}, ...
    'kappa_lower',{},'kappa_upper',{},'idx_transition',{});
cellIdx = 0;

t0_all = tic;
for ic = 1:nC
    factor = factors(ic);
    for iR = 1:nR
        R2 = R2s(iR);
        spaceScale = spaceScaleMap(R2);
        m = R2/(2*G)*c^2*factor;
        for iB = 1:nB
            beta = betas(iB);
            cellIdx = cellIdx + 1;
            C = factor;     % by construction
            % Inner Delta candidates
            Deltas = kappa_grid .* beta ./ C .* R2;
            % Cap Delta at R2-0.5 (else R1 <= 0.5 -> grid issues)
            Deltas = min(Deltas, R2 - 0.5);
            % And Delta > 0
            valid = Deltas > 0.05*R2;
            DeltasUse = Deltas(valid);
            kappasUse = kappa_grid(valid);
            nKuse = numel(DeltasUse);

            fprintf('\n[%s] CELL %d/%d  factor=%.4f (C=%.4f)  R2=%g  beta=%g  m=%.3e\n', ...
                datestr(now,'HH:MM:SS'), cellIdx, nCells, factor, C, R2, beta, m);
            fprintf('  Deltas to scan: '); fprintf('%.3f ', DeltasUse); fprintf('\n');

            passDEC = zeros(1,nKuse); passNEC = zeros(1,nKuse);
            passWEC = zeros(1,nKuse); passSEC = zeros(1,nKuse);
            minDEC  = zeros(1,nKuse);

            % Build grid (R2-dependent only)
            if centered == 1
                gridSize = ceil([1,2*(R2+10)*spaceScale,2*(R2+10)*spaceScale,cartoonThickness]);
            else
                gridSize = ceil([1,(R2+10)*spaceScale,(R2+10)*spaceScale,cartoonThickness]);
            end
            gridScaling = [1/(timeScale*spaceScale*((beta)*c+1)),1/spaceScale,1/spaceScale,1/spaceScale];
            gridScaling(1) = 1/(1000*c);
            if centered == 1
                worldCenter = [(cartoonThickness+1)/2,(2*(R2+10)*spaceScale+1)/2,(2*(R2+10)*spaceScale+1)/2,(cartoonThickness+1)/2].*gridScaling;
                xc = linspace(0,2*(R2+10),gridSize(2)-4)';
                yc = linspace(0,2*(R2+10),gridSize(3)-4)';
            else
                worldCenter = [(cartoonThickness+1)/2,5,5,(cartoonThickness+1)/2].*gridScaling;
                xc = linspace(0,(R2+10),gridSize(2)-4)';
                yc = linspace(0,(R2+10),gridSize(3)-4)';
            end
            [Xg,Yg] = meshgrid(xc,yc);
            xcent = Xg - mean(xc);  ycent = Yg - mean(yc);
            r2grid = xcent.^2 + ycent.^2;

            for iK = 1:nKuse
                Delta = DeltasUse(iK);
                R1 = R2 - Delta;

                Metric = metricGet_WarpShellComoving(gridSize,worldCenter,m,R1,R2,Rbuff,sigma,smoothFactor,beta,doWarp,gridScaling);
                EC = evalMetric(Metric,1,1);

                zIdx = round((cartoonThickness+1)/2);
                nec = squeeze(EC.null    (1,3:end-2,3:end-2,zIdx))';
                wec = squeeze(EC.weak    (1,3:end-2,3:end-2,zIdx))';
                dec = squeeze(EC.dominant(1,3:end-2,3:end-2,zIdx))';
                sec = squeeze(EC.strong  (1,3:end-2,3:end-2,zIdx))';

                shellMask = (r2grid >= R1^2) & (r2grid <= R2^2);
                nMask = nnz(shellMask);
                passNEC(iK) = sum(nec(shellMask) >= tol) / nMask;
                passWEC(iK) = sum(wec(shellMask) >= tol) / nMask;
                passDEC(iK) = sum(dec(shellMask) >= tol) / nMask;
                passSEC(iK) = sum(sec(shellMask) >= tol) / nMask;
                minDEC(iK)  = min(dec(shellMask));

                fprintf('    Delta=%6.3f  kappa=%5.2f  NEC=%.4f WEC=%.4f DEC=%.4f SEC=%.4f  minDEC=%+.2e\n', ...
                    Delta, kappasUse(iK), passNEC(iK), passWEC(iK), passDEC(iK), passSEC(iK), minDEC(iK));
            end

            % Find transition: largest iK with passDEC < 1 (lower bracket),
            %                  smallest iK with passDEC == 1 (upper bracket).
            passOK = (passDEC >= 1 - 1e-9);
            firstOK = find(passOK, 1, 'first');
            if isempty(firstOK)
                kappa_lower = kappasUse(end);   % even widest didn't pass
                kappa_upper = NaN;              % unbounded above
                idx_trans = NaN;
            elseif firstOK == 1
                kappa_lower = NaN;              % even narrowest passed
                kappa_upper = kappasUse(1);
                idx_trans = 1;
            else
                kappa_lower = kappasUse(firstOK-1);
                kappa_upper = kappasUse(firstOK);
                idx_trans = firstOK;
            end

            results(cellIdx).factor      = factor;
            results(cellIdx).C           = C;
            results(cellIdx).R2          = R2;
            results(cellIdx).beta        = beta;
            results(cellIdx).m           = m;
            results(cellIdx).Deltas      = DeltasUse;
            results(cellIdx).kappas_grid = kappasUse;
            results(cellIdx).passDEC     = passDEC;
            results(cellIdx).passNEC     = passNEC;
            results(cellIdx).passWEC     = passWEC;
            results(cellIdx).passSEC     = passSEC;
            results(cellIdx).minDEC_inshell = minDEC;
            results(cellIdx).spaceScale  = spaceScale;
            results(cellIdx).gridSize    = gridSize;
            results(cellIdx).kappa_lower = kappa_lower;
            results(cellIdx).kappa_upper = kappa_upper;
            results(cellIdx).idx_transition = idx_trans;

            fprintf('  -> kappa transition: (%.3g, %.3g]\n', kappa_lower, kappa_upper);
            elapsed = toc(t0_all);
            eta = elapsed/cellIdx*(nCells-cellIdx)/60;
            fprintf('  Elapsed %.1f min, ETA %.1f min\n', elapsed/60, eta);
        end
    end
end

%% Save raw .mat
save('kappa_surface_sweep.mat','results','factors','R2s','betas','kappa_grid', ...
    'spaceScaleMap','-v7');
fprintf('\nSaved kappa_surface_sweep.mat\n');

%% Flat CSV
fid = fopen('kappa_surface_sweep.csv','w');
fprintf(fid,'factor,C,R2,beta,m,spaceScale,kappa_lower,kappa_upper,kappa_mid\n');
for i = 1:numel(results)
    r = results(i);
    if isnan(r.kappa_lower) && ~isnan(r.kappa_upper)
        kmid = r.kappa_upper / 2;       % only upper known
    elseif ~isnan(r.kappa_lower) && isnan(r.kappa_upper)
        kmid = r.kappa_lower * 1.5;     % only lower known (extrapolate)
    elseif isnan(r.kappa_lower) && isnan(r.kappa_upper)
        kmid = NaN;
    else
        kmid = 0.5*(r.kappa_lower + r.kappa_upper);
    end
    fprintf(fid,'%.6f,%.6f,%g,%g,%.6e,%d,%.6f,%.6f,%.6f\n', ...
        r.factor, r.C, r.R2, r.beta, r.m, r.spaceScale, ...
        r.kappa_lower, r.kappa_upper, kmid);
end
fclose(fid);
fprintf('Saved kappa_surface_sweep.csv\n');

%% Summary printout
fprintf('\n=== SUMMARY: kappa transition brackets across (factor, R2, beta) ===\n');
fprintf('factor   C        R2     beta      kappa_lower  kappa_upper  kappa_mid\n');
for i = 1:numel(results)
    r = results(i);
    if isnan(r.kappa_lower) && ~isnan(r.kappa_upper)
        kmid = r.kappa_upper / 2;
    elseif ~isnan(r.kappa_lower) && isnan(r.kappa_upper)
        kmid = r.kappa_lower * 1.5;
    elseif isnan(r.kappa_lower) && isnan(r.kappa_upper)
        kmid = NaN;
    else
        kmid = 0.5*(r.kappa_lower + r.kappa_upper);
    end
    fprintf('%.4f  %.4f   %3g   %.3f      %.3f         %.3f         %.3f\n', ...
        r.factor, r.C, r.R2, r.beta, r.kappa_lower, r.kappa_upper, kmid);
end

%% Spread statistics
kmids = arrayfun(@(r) ...
    (isnan(r.kappa_lower)*r.kappa_upper/2 ...
     + (~isnan(r.kappa_lower)&isnan(r.kappa_upper))*r.kappa_lower*1.5 ...
     + (~isnan(r.kappa_lower)&~isnan(r.kappa_upper))*0.5*(r.kappa_lower+r.kappa_upper)), ...
    results);
kmids_finite = kmids(~isnan(kmids));
fprintf('\n--- kappa midpoint statistics (n=%d) ---\n', numel(kmids_finite));
fprintf('  mean    = %.3f\n', mean(kmids_finite));
fprintf('  median  = %.3f\n', median(kmids_finite));
fprintf('  std     = %.3f\n', std(kmids_finite));
fprintf('  range   = [%.3f, %.3f]\n', min(kmids_finite), max(kmids_finite));
fprintf('  rel std = %.1f%%  (decision-gate-A: <10%% => kappa is universal)\n', ...
    100*std(kmids_finite)/mean(kmids_finite));

%% Diagnostic plots
try
    fig = figure('Visible','off','Position',[100 100 1200 800]);

    % Plot 1: kappa midpoint vs beta, coloured by C, marker by R2
    subplot(2,2,1); hold on;
    R2_markers = containers.Map({15,20,30},{'o','s','^'});
    C_colors = lines(nC);
    for i = 1:numel(results)
        r = results(i);
        kmid = kmids(i);
        if isnan(kmid), continue; end
        cIdx = find(factors == r.factor, 1);
        plot(r.beta, kmid, R2_markers(r.R2), ...
            'MarkerFaceColor', C_colors(cIdx,:), 'MarkerEdgeColor','k', 'MarkerSize',8);
    end
    xlabel('\beta = v_{warp}/c'); ylabel('\kappa midpoint');
    title('\kappa vs \beta (color: C, marker: R_2)'); grid on;
    set(gca,'XScale','log');

    % Plot 2: kappa midpoint vs C
    subplot(2,2,2); hold on;
    for i = 1:numel(results)
        r = results(i);
        kmid = kmids(i);
        if isnan(kmid), continue; end
        plot(r.C, kmid, 'o', 'MarkerFaceColor',[0.2 0.5 0.8], 'MarkerSize',8);
    end
    xlabel('C = 2GM/(R_2 c^2)'); ylabel('\kappa midpoint');
    title('\kappa vs C'); grid on;

    % Plot 3: kappa midpoint vs R2
    subplot(2,2,3); hold on;
    for i = 1:numel(results)
        r = results(i);
        kmid = kmids(i);
        if isnan(kmid), continue; end
        plot(r.R2, kmid, 'o', 'MarkerFaceColor',[0.8 0.4 0.2], 'MarkerSize',8);
    end
    xlabel('R_2 [m]'); ylabel('\kappa midpoint');
    title('\kappa vs R_2'); grid on;

    % Plot 4: histogram of kappa midpoints
    subplot(2,2,4);
    histogram(kmids_finite, 'BinMethod','auto', 'FaceColor',[0.4 0.6 0.4]);
    xlabel('\kappa midpoint'); ylabel('count');
    title(sprintf('Distribution: mean=%.2f, std=%.2f (rel %.1f%%)', ...
        mean(kmids_finite), std(kmids_finite), 100*std(kmids_finite)/mean(kmids_finite)));
    grid on;

    sgtitle('Task 3.2: \kappa-surface sweep across (M, R_2, \beta)');
    saveas(fig, 'kappa_surface_sweep.png');
    fprintf('Saved kappa_surface_sweep.png\n');
    close(fig);
catch ME
    fprintf('Plot generation failed: %s\n', ME.message);
end

fprintf('\n=== DONE === Total wallclock: %.1f min\n', toc(t0_all)/60);
