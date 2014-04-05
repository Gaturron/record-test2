function [Cepstra, FBEnergy] = wav2mfcc( wavFilename, tWindow, tStep, alpha, freqRange, fbChannels, numCep, lifter )

%   Mel frequency cepstral coefficient feature extraction.
%
%   wav2mfcc
%   (wavFilename, tWindow, tStep, alpha, freqRange, fbChannels, numCep, lifterexp) 
%   returns mel frequency cepstral coefficients (MFCCs) computed from speech
%   signal given a waveform filename. The speech signal is first 
%   preemphasised using a first order FIR filter with preemphasis 
%   coefficient ALPHA. The preemphasised speech signal is subjected 
%   to the short-time Fourier transform analysis with frame durations 
%   of tWindow (ms), frame shifts of tStep (ms) and a hamming analysis window
%   This is followed by magnitude spectrum computation followed by 
%   filterbank design with fbChannels triangular filters uniformly spaced 
%   on the mel scale between lower and upper frequency limits given in 
%   freqRange (Hz). 
%   The filterbank is applied to the magnitude spectrum values to produce 
%   filterbank energies FBE. Log-compressed FBEs are then decorrelated using 
%   the discrete cosine transform to produce cepstral coefficients. Final
%   step applies sinusoidal lifter to produce liftered MFCCs that 
%   closely match those produced by HTK [1].
%
%
%   This framework is based on Dan Ellis' rastamat routines [2]. The 
%   emphasis is placed on closely matching MFCCs produced by HTK [1]
%   (refer to p.337 of [1] for HTK's defaults) with simplicity and 
%   compactness as main considerations, but at a cost of reduced 
%   flexibility. This routine is meant to be easy to extend, and as 
%   a starting point for work with cepstral coefficients in MATLAB.
%   The triangular filterbank equations are given in [3].
%
%   Inputs
%           wavFilename: input speech filename
%
%           tWindow: analysis frame duration (ms) 
% 
%           tStep: analysis frame shift (ms)
%
%           ALPHA: preemphasis coefficient
% 
%           freqRange: frequency range (Hz) for filterbank analysis
%
%           fbChannels: number of filterbank channels
%
%           numCep: number of cepstral coefficients (including the 0th coeff)
%
%           lifter: liftering parameter
%
%   Outputs
%           Cepstra: matrix of mel frequency cepstral coefficients (MFCCs)
%           where the feature vectors are in columns
%
%           FBE is a matrix of filterbank energies
%               with feature vectors as columns
%
%
%
%   References
%
%           [1] Young, S., Evermann, G., Gales, M., Hain, T., Kershaw, D., 
%               Liu, X., Moore, G., Odell, J., Ollason, D., Povey, D., 
%               Valtchev, V., Woodland, P., 2006. The HTK Book (for HTK 
%               Version 3.4.1). Engineering Department, Cambridge University.
%               (see also: http://htk.eng.cam.ac.uk)
%
%           [2] Ellis, D., 2005. Reproducing the feature outputs of 
%               common programs using Matlab and melfcc.m. url: 
%               http://labrosa.ee.columbia.edu/matlab/rastamat/mfccs.html
%
%           [3] Huang, X., Acero, A., Hon, H., 2001. Spoken Language 
%               Processing: A guide to theory, algorithm, and system 
%               development. Prentice Hall, Upper Saddle River, NJ, 
%               USA (pp. 314-315).
%
%   See also EXAMPLE, COMPARE, FRAMES2VEC, TRIFBANK.

%   Author: Kamil Wojcicki, September 2011


    %% PRELIMINARIES 

    % Check the number of inputs
    if( nargin~= 8 ), help mfcc; return; end; 

    % Load speech signal and sampling frequency
    try 
        [inputWaveform, fs] = wavread(wavFilename);
    catch
        disp('Waveform File not found');
    end
    
    % Apply mean substraction
    meansubstraction = 1;
    if meansubstraction
        inputWaveform = inputWaveform - mean(inputWaveform);
    end
    
    % Explode samples to the range of 16 bit shorts
    if( max(abs(inputWaveform))<=1 ), inputWaveform = inputWaveform * 2^15; end;

    Nw = round( 1E-3*tWindow*fs );      % frame duration (samples)
    Ns = round( 1E-3*tStep*fs );        % frame shift (samples)

    nfft = 2^nextpow2( Nw );     % length of FFT analysis 
    K = nfft/2+1;                % length of the unique part of the FFT 


    %% HANDY INLINE FUNCTION HANDLES

    % hamming window (see Eq. (5.2) on p.73 of [1])
    hamming = @(N)(0.54-0.46*cos(2*pi*[0:N-1].'/(N-1)));
    
    % Forward and backward mel frequency warping (see Eq. (5.13) on p.76 of [1]) 
    % Note that base 10 is used in [1], while base e is used here and in HTK code
    hz2mel = @( hz )( 1127*log(1+hz/700) );     % Hertz to mel warping function
    mel2hz = @( mel )( 700*exp(mel/1127)-700 ); % mel to Hertz warping function

    % Type III DCT matrix routine (see Eq. (5.14) on p.77 of [1])
    dctm = @( N, M )( sqrt(2.0/M) * cos( repmat([0:N-1].',1,M) ...
                                       .* repmat(pi*([1:M]-0.5)/M,N,1) ) );

    % Cepstral lifter routine (see Eq. (5.12) on p.75 of [1])
    ceplifter = @( N, L )( 1+0.5*L*sin(pi*[0:N-1]/L) );


    %% FEATURE EXTRACTION 

    % Preemphasis filtering (see Eq. (5.1) on p.73 of [1])
    inputWaveform = filter( [1 -alpha], 1, inputWaveform );

    % Framing and windowing (frames as columns)
    frames = vec2frames( inputWaveform, Nw, Ns, 'cols', hamming, false );

    % Magnitude spectrum computation (as column vectors)
    MAG = abs( fft(frames,nfft,1) ); 

    % Triangular filterbank with uniformly spaced filters on mel scale
    H = trifbank( fbChannels, K, freqRange, fs, hz2mel, mel2hz ); % size of H is M x K 

    % Filterbank application to unique part of the magnitude spectrum
    FBEnergy = H * MAG(1:K,:); % FBE( FBE<1.0 ) = 1.0; % apply mel floor

    % DCT matrix computation
    DCT = dctm( numCep, fbChannels );

    % Conversion of logFBEs to cepstral coefficients through DCT
    Cepstra =  DCT * log( FBEnergy );

    % Cepstral lifter computation
    lifter = ceplifter( numCep, lifter );

    % Cepstral liftering gives liftered cepstral coefficients
    Cepstra = diag( lifter ) * Cepstra; % ~ HTK's MFCCs


% EOF
