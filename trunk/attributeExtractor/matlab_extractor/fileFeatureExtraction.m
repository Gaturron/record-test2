%batchFeatureExtraction('/home/fernando/Descargas/FeatureExtraction/');
function [res] = fileFeatureExtraction(filepath)
%=========================================================================
% batchFeatureExtraction - Computes and writes MFCC's for a set of speech waveform.
% 
% Input parameters: folderPath - path to the folder with input waveforms
%
%
% Diego Evin
% July 10, 2013
% diegoevin_at_gmail.com
%=========================================================================

disp('empieza a extraer path: ');

tWindow = 25; %100;                % analysis frame duration (ms)
tStep = 10;                 % analysis frame shift (ms)
alpha = 0.97;                 % preemphasis coefficient
freqRange = [ 50 3800 ];       % frequency range to consider
fbChannels = 25;            % number of filterbank channels 
numCep = 33;                % number of cepstral coefficients
lifter = 22;                % cepstral sine lifter parameter

filename=[ filepath ];
[ CC, FBE] = wav2mfcc( filename, tWindow, tStep, alpha, freqRange, fbChannels, numCep, lifter );
[nCeps, nframes] = size(CC);
    
for i=1:nframes
    for j=1:nCeps
        res(i, j) = CC(j, i);
    end
end

end
