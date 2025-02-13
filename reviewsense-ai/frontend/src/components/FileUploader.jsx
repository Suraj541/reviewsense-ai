import React, { useState } from 'react';

const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async (type) => {
    const formData = new FormData();
    formData.append('file', file);

    const endpoint = type === 'excel' 
      ? '/analyze/excel' 
      : '/analyze/pdf';

    const response = await fetch(endpoint, {
      method: 'POST',
      body: formData
    });

    if (type === 'excel') {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'analysis_report.xlsx';
      a.click();
    } else {
      setResult(await response.json());
    }
  };

  return (
    <div className="file-upload-section">
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <div className="button-group">
        <button onClick={() => handleUpload('excel')}>
          Analyze Excel
        </button>
        <button onClick={() => handleUpload('pdf')}>
          Analyze PDF
        </button>
      </div>
      {result && (
        <div className="pdf-results">
          <h3>PDF Analysis Results</h3>
          <p>Sentiment: {result.sentiment}</p>
          <p>Confidence: {result.confidence}</p>
          <div className="original-text">
            {result.original_text}
          </div>
        </div>
      )}
    </div>
  );
};
