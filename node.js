const express = require('express');
const { GoogleSpreadsheet } = require('google-spreadsheet');

const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.redirect('/growth-stage');
});

app.get('/growth-stage', async (req, res) => {
  const doc = new GoogleSpreadsheet('1BZJxVbcTFnRLpS3dP8ZBzBPfN0YmztBO_6jLP4di9hc');
  await doc.useServiceAccountAuth(require('./researchprojectgrowth-5ec60156b11a.json'));
  await doc.loadInfo();

  const sheet = doc.sheetsByTitle['growth']; // assuming the sheet name is 'growth'
  await sheet.loadCells('B1'); // Load only the B1 cell

  const cell = sheet.getCellByA1('B1');
  const growthStage = cell.value;
  
  res.send(growthStage);
});

app.listen(port, '0.0.0.0', () => {
    console.log(`Server listening at http://localhost:${port}`);
  });