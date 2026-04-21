% kappa_sweep.m
% 2A.9b -- numerical kappa bracket from Warp Factory.
% Holds M = 4.49e27 kg, vWarp = 0.02 c, R2 = 20 m fixed; varies Delta = R2 - R1.
% Finds Delta_min where DEC first develops in-shell failures, converts to kappa.

addpath(genpath(pwd));

%% Fixed params (Fuchs canonical)
spaceScale = 5;
timeScale = 1;
centered = 1;
cartoonThickness = 5;
R2 = 20;
Rbuff = 0;
factor = 1/3;
m = R2/(2*G)*c^2*factor;       % ~4.49e27 kg
vWarp = 0.02;
sigma = 0;
doWarp = 1;
smoothFactor = 4000;

C_compactness = 2*G*m / (R2*c^2);  % = factor = 1/3
fprintf('Fixed: m=%.3e kg, R2=%g m, vWarp=%g, C=2GM/(Rc^2)=%.4f\n', m, R2, vWarp, C_compactness);

%% Sweep Delta
Deltas = [1.0, 1.5, 2.0, 3.0, 5.0, 7.0, 10.0];
nD = numel(Deltas);
results = struct('Delta',{}, 'R1',{}, 'passNEC',{}, 'passWEC',{}, 'passDEC',{}, 'passSEC',{}, 'minDEC',{});

for i = 1:nD
    Delta = Deltas(i);
    R1 = R2 - Delta;
    fprintf('\n[%s] (%d/%d) Delta=%g, R1=%g, R2=%g\n', datestr(now,'HH:MM:SS'), i, nD, Delta, R1, R2);

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

    Metric = metricGet_WarpShellComoving(gridSize,worldCenter,m,R1,R2,Rbuff,sigma,smoothFactor,vWarp,doWarp,gridScaling);
    EC = evalMetric(Metric,1,1);

    zIdx = round((cartoonThickness+1)/2);
    nec = squeeze(EC.null   (1,3:end-2,3:end-2,zIdx))';
    wec = squeeze(EC.weak   (1,3:end-2,3:end-2,zIdx))';
    dec = squeeze(EC.dominant(1,3:end-2,3:end-2,zIdx))';
    sec = squeeze(EC.strong (1,3:end-2,3:end-2,zIdx))';

    xc = X - mean(x);  yc = Y - mean(y);
    r2 = xc.^2 + yc.^2;
    shellMask = (r2 >= R1^2) & (r2 <= R2^2);

    tol = -1e-12;
    passNEC = sum(nec(shellMask) >= tol) / nnz(shellMask);
    passWEC = sum(wec(shellMask) >= tol) / nnz(shellMask);
    passDEC = sum(dec(shellMask) >= tol) / nnz(shellMask);
    passSEC = sum(sec(shellMask) >= tol) / nnz(shellMask);
    minDEC  = min(dec(shellMask));

    fprintf('   NEC=%.4f  WEC=%.4f  DEC=%.4f  SEC=%.4f   min(DEC|shell)=%+.3e\n', ...
        passNEC,passWEC,passDEC,passSEC,minDEC);

    results(i).Delta   = Delta;
    results(i).R1      = R1;
    results(i).passNEC = passNEC;
    results(i).passWEC = passWEC;
    results(i).passDEC = passDEC;
    results(i).passSEC = passSEC;
    results(i).minDEC  = minDEC;
end

%% Summary
fprintf('\n=== SUMMARY (m=%.3e kg, R2=%g m, vWarp=%g, C=%.4f) ===\n', m, R2, vWarp, C_compactness);
fprintf('  Delta[m]    R1[m]    passNEC  passWEC  passDEC  passSEC   min(DEC|shell)   kappa=Delta*C/(beta*R2)\n');
for i = 1:nD
    kappa_i = results(i).Delta * C_compactness / (vWarp * R2);
    fprintf('  %7.2f   %6.2f    %.4f   %.4f   %.4f   %.4f   %+.3e   %.4f\n', ...
        results(i).Delta, results(i).R1, results(i).passNEC, results(i).passWEC, ...
        results(i).passDEC, results(i).passSEC, results(i).minDEC, kappa_i);
end
fprintf('Analytic bracket (ROADMAP 2A.9a): kappa in [0.05, 0.875]\n');

save('kappa_sweep.mat','Deltas','results','m','R2','vWarp','C_compactness','-v7');
fprintf('\nSaved: kappa_sweep.mat\n');
