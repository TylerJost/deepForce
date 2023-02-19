clc
clear

files = dir('../data/raw');
files = {files.name};
filesClean = {};
c = 1;
% Get rid of non .mat files that dir() produces
for file = 1:length(files)
  if endsWith(files{file}, '.mat')
    filesClean{c} = files{file};
    c = c + 1;
  end
end

% For each file load in the force plate data
for idx = 1:length(filesClean)
  fprintf('Iter %g / %g \n', idx, length(filesClean))
  ForcePlateData = load(fullfile('..', 'data', 'raw', filesClean{1}), 'ForcePlateData', 'ForcePlateData');

  fp = ForcePlateData.ForcePlateData;
  fpFields = fields(fp);

  % For all force plates (should just be 'Plate 2' and 'Plate 3'
  % Concatenate everything into one table and save
  allFP = {};
  for fpNum = 1:length(fpFields)
    cat1 = join(fp.(fpFields{fpNum}).Moment, fp.(fpFields{fpNum}).Force);
    fullFP = join(cat1, fp.(fpFields{fpNum}).Center);
    cols = fullFP.Properties.VariableNames;
    
    
    cols = strcat(cols, strcat('-', fpFields{fpNum}));
    cols{1} = 'Frame';
    cols{2} = 'Subframe';

    fullFP.Properties.VariableNames = cols; 
    allFP{fpNum} = fullFP;
  end
  % Note: Only works if there are 2 forceplates
  allFP = join(allFP{1}, allFP{2});
  % Get proper name and save
  fileParts = split(filesClean{idx},'.mat');
  name = strcat(fileParts{1}, '.csv');
  fullPathWrite = fullfile('..', 'data', 'interim', name);
  writetable(allFP, fullPathWrite);
end

