/**
 * Function to initialize the Razeco Performance Dashboard with sample data
 * This would normally be executed once to set up the initial structure
 */
function initializeDashboard() {
  // Spreadsheet ID für das Dashboard
  var spreadsheetId = '19s3l4JgQz5U6jw3lgvO9LHlKGvDdzQPpEKMeteqnUqY';
  var ss = SpreadsheetApp.openById(spreadsheetId);
  
  // Bestehende Sheets
  var tabellenblatt1 = ss.getSheets()[0];
  
  // Umbenennen und Struktur einrichten
  tabellenblatt1.setName('Creatives KPIs');
  
  // Headers für Creatives KPIs
  var creativesHeaders = [
    'Monat', 'Kanal', 'Kampagne', 'Creative ID', 'Creative Name', 
    'Format', 'Impressions', 'Clicks', 'CTR', 'CPC',
    'Spend', 'Conversions', 'CPA', 'ROAS', 'Umsatz'
  ];
  tabellenblatt1.getRange(1, 1, 1, creativesHeaders.length).setValues([creativesHeaders]);
  
  // Neue Sheets erstellen
  var adSetsSheet = ss.insertSheet('Ad Sets KPIs');
  var dashboardSheet = ss.insertSheet('Dashboard');
  var scheduleSheet = ss.insertSheet('Update Schedule');
  
  // Headers für Ad Sets KPIs
  var adSetsHeaders = [
    'Monat', 'Kanal', 'Kampagne', 'Ad Set ID', 'Ad Set Name', 
    'Targeting', 'Budget', 'Impressions', 'Clicks', 'CTR', 'CPC',
    'Spend', 'Conversions', 'CPA', 'ROAS', 'Umsatz'
  ];
  adSetsSheet.getRange(1, 1, 1, adSetsHeaders.length).setValues([adSetsHeaders]);
  
  // Headers für Schedule
  var scheduleHeaders = [
    'Datenquelle', 'Letzte Aktualisierung', 'Nächste Aktualisierung', 
    'Verantwortlicher', 'Status', 'Notizen'
  ];
  scheduleSheet.getRange(1, 1, 1, scheduleHeaders.length).setValues([scheduleHeaders]);
  
  // Datenquellen hinzufügen
  var dataSources = [
    ['Facebook Ads', new Date(), '', 'Automatisch', 'Aktiv', 'Monatlich am 1.'],
    ['Google Ads', new Date(), '', 'Automatisch', 'Aktiv', 'Monatlich am 1.'],
    ['TikTok Ads', new Date(), '', 'Automatisch', 'Aktiv', 'Monatlich am 1.'],
    ['Analytics', new Date(), '', 'Automatisch', 'Aktiv', 'Monatlich am 1.']
  ];
  scheduleSheet.getRange(2, 1, dataSources.length, scheduleHeaders.length).setValues(dataSources);
  
  // Dashboard einrichten
  dashboardSheet.getRange('A1').setValue('RAZECO PERFORMANCE DASHBOARD');
  dashboardSheet.getRange('A1:F1').merge();
  dashboardSheet.getRange('A1').setFontSize(18).setFontWeight('bold');
  
  // Datum hinzufügen
  dashboardSheet.getRange('A2').setValue('Letzte Aktualisierung:');
  dashboardSheet.getRange('B2').setValue(new Date()).setNumberFormat('dd.MM.yyyy');
  
  // Beispieldaten für Januar hinzufügen
  addSampleMonthData(ss, 'Januar');
  
  // Beispieldaten für Februar hinzufügen
  addSampleMonthData(ss, 'Februar');
  
  // Format für alle Header
  formatHeaders(ss);
  
  // Zahlenformate anwenden
  applyNumberFormats(ss);
  
  // Dashboard mit Diagrammen einrichten
  setupDashboardVisuals(dashboardSheet);
  
  // Datenvalidierung hinzufügen
  addDataValidation(ss);
  
  // Farbkodierung
  applyConditionalFormatting(ss);
}

/**
 * Fügt Beispieldaten für einen bestimmten Monat hinzu
 */
function addSampleMonthData(ss, month) {
  var creativesSheet = ss.getSheetByName('Creatives KPIs');
  var adSetsSheet = ss.getSheetByName('Ad Sets KPIs');
  
  // Zufallsfaktor für Variation zwischen Monaten
  var factor = month === 'Januar' ? 0.9 : 1.1;
  
  // Beispieldaten für Creatives
  var creativesData = [
    [month, 'Facebook', 'Sommer-Sale', 'CR001', 'Hautpflege-Video', '9:16', Math.round(125000 * factor), Math.round(3200 * factor), 0.0256, 0.45 * factor, 1440 * factor, Math.round(52 * factor), 27.69 * factor, 3.2 * factor, 4608 * factor],
    [month, 'Facebook', 'Sommer-Sale', 'CR002', 'Produktvorstellung', '1:1', Math.round(98000 * factor), Math.round(2100 * factor), 0.0214, 0.51 * factor, 1071 * factor, Math.round(38 * factor), 28.18 * factor, 2.8 * factor, 2999 * factor],
    [month, 'Instagram', 'Neukunden', 'CR003', 'Testimonial Sarah', '4:5', Math.round(156000 * factor), Math.round(4800 * factor), 0.0308, 0.38 * factor, 1824 * factor, Math.round(63 * factor), 28.95 * factor, 3.5 * factor, 6384 * factor],
    [month, 'Google', 'Remarketing', 'CR004', 'Rabatt-Banner', '16:9', Math.round(45000 * factor), Math.round(980 * factor), 0.0218, 0.65 * factor, 637 * factor, Math.round(22 * factor), 28.95 * factor, 2.9 * factor, 1847 * factor],
    [month, 'TikTok', 'Brand-Awareness', 'CR005', 'Challenge-Video', '9:16', Math.round(210000 * factor), Math.round(5400 * factor), 0.0257, 0.42 * factor, 2268 * factor, Math.round(41 * factor), 55.32 * factor, 1.9 * factor, 4309 * factor]
  ];
  
  // Beispieldaten für Ad Sets
  var adSetsData = [
    [month, 'Facebook', 'Sommer-Sale', 'AS001', 'Lookalike 1%', 'Lookalike Audience', 30 * factor, Math.round(110000 * factor), Math.round(2800 * factor), 0.0255, 0.47 * factor, 1316 * factor, Math.round(45 * factor), 29.24 * factor, 3.1 * factor, 4080 * factor],
    [month, 'Facebook', 'Sommer-Sale', 'AS002', 'Interesse Beauty', 'Interessen-Targeting', 25 * factor, Math.round(113000 * factor), Math.round(2500 * factor), 0.0221, 0.49 * factor, 1225 * factor, Math.round(45 * factor), 27.22 * factor, 2.9 * factor, 3553 * factor],
    [month, 'Instagram', 'Neukunden', 'AS003', 'Frauen 25-34', 'Demografisch', 40 * factor, Math.round(156000 * factor), Math.round(4800 * factor), 0.0308, 0.38 * factor, 1824 * factor, Math.round(63 * factor), 28.95 * factor, 3.5 * factor, 6384 * factor],
    [month, 'Google', 'Remarketing', 'AS004', 'Website-Besucher', 'Remarketing', 20 * factor, Math.round(45000 * factor), Math.round(980 * factor), 0.0218, 0.65 * factor, 637 * factor, Math.round(22 * factor), 28.95 * factor, 2.9 * factor, 1847 * factor],
    [month, 'TikTok', 'Brand-Awareness', 'AS005', 'Ähnliche Zielgruppe', 'Lookalike', 35 * factor, Math.round(210000 * factor), Math.round(5400 * factor), 0.0257, 0.42 * factor, 2268 * factor, Math.round(41 * factor), 55.32 * factor, 1.9 * factor, 4309 * factor]
  ];
  
  // Daten in die Tabelle einfügen
  var nextCreativesRow = getNextEmptyRow(creativesSheet);
  creativesSheet.getRange(nextCreativesRow, 1, creativesData.length, creativesData[0].length).setValues(creativesData);
  
  var nextAdSetsRow = getNextEmptyRow(adSetsSheet);
  adSetsSheet.getRange(nextAdSetsRow, 1, adSetsData.length, adSetsData[0].length).setValues(adSetsData);
}

/**
 * Findet die nächste leere Zeile in einem Tabellenblatt
 */
function getNextEmptyRow(sheet) {
  var values = sheet.getDataRange().getValues();
  
  for (var i = 0; i < values.length; i++) {
    var row = values[i];
    var isEmpty = true;
    
    for (var j = 0; j < row.length; j++) {
      if (row[j] !== '') {
        isEmpty = false;
        break;
      }
    }
    
    if (isEmpty) {
      return i + 1; // 1-basierter Index
    }
  }
  
  return values.length + 1; // Nach der letzten Zeile
}

/**
 * Formatiert alle Header-Zeilen
 */
function formatHeaders(ss) {
  var sheets = ss.getSheets();
  for (var i = 0; i < sheets.length; i++) {
    var headerRange = sheets[i].getRange(1, 1, 1, sheets[i].getLastColumn());
    headerRange.setBackground('#4285F4');
    headerRange.setFontColor('#FFFFFF');
    headerRange.setFontWeight('bold');
  }
}

/**
 * Wendet Zahlenformate an
 */
function applyNumberFormats(ss) {
  // Formatting for numbers in Creatives sheet
  var creativeSheet = ss.getSheetByName('Creatives KPIs');
  creativeSheet.getRange('G2:G1000').setNumberFormat('#,##0'); // Impressions
  creativeSheet.getRange('H2:H1000').setNumberFormat('#,##0'); // Clicks
  creativeSheet.getRange('I2:I1000').setNumberFormat('0.00%'); // CTR
  creativeSheet.getRange('J2:J1000').setNumberFormat('0.00 €'); // CPC
  creativeSheet.getRange('K2:K1000').setNumberFormat('0.00 €'); // Spend
  creativeSheet.getRange('L2:L1000').setNumberFormat('#,##0'); // Conversions
  creativeSheet.getRange('M2:M1000').setNumberFormat('0.00 €'); // CPA
  creativeSheet.getRange('N2:N1000').setNumberFormat('0.00'); // ROAS
  creativeSheet.getRange('O2:O1000').setNumberFormat('0.00 €'); // Umsatz
  
  // Formatting for numbers in Ad Sets sheet
  var adSetsSheet = ss.getSheetByName('Ad Sets KPIs');
  adSetsSheet.getRange('G2:G1000').setNumberFormat('0.00 €'); // Budget
  adSetsSheet.getRange('H2:H1000').setNumberFormat('#,##0'); // Impressions
  adSetsSheet.getRange('I2:I1000').setNumberFormat('#,##0'); // Clicks
  adSetsSheet.getRange('J2:J1000').setNumberFormat('0.00%'); // CTR
  adSetsSheet.getRange('K2:K1000').setNumberFormat('0.00 €'); // CPC
  adSetsSheet.getRange('L2:L1000').setNumberFormat('0.00 €'); // Spend
  adSetsSheet.getRange('M2:M1000').setNumberFormat('#,##0'); // Conversions
  adSetsSheet.getRange('N2:N1000').setNumberFormat('0.00 €'); // CPA
  adSetsSheet.getRange('O2:O1000').setNumberFormat('0.00'); // ROAS
  adSetsSheet.getRange('P2:P1000').setNumberFormat('0.00 €'); // Umsatz
}

/**
 * Richtet das Dashboard-Blatt mit Visualisierungen ein
 */
function setupDashboardVisuals(dashboardSheet) {
  // Abschnitt hinzufügen
  dashboardSheet.getRange('A4').setValue('PERFORMANCE ÜBERSICHT');
  dashboardSheet.getRange('A4:F4').merge();
  dashboardSheet.getRange('A4').setFontSize(14).setFontWeight('bold');
  
  // KPI-Boxen
  var kpiLabels = ['Gesamtausgaben', 'Impressions', 'Clicks', 'Conversions', 'Durchschn. CPA', 'ROAS'];
  var kpiFormulas = [
    '=SUM(\'Creatives KPIs\'!K2:K1000)',
    '=SUM(\'Creatives KPIs\'!G2:G1000)',
    '=SUM(\'Creatives KPIs\'!H2:H1000)',
    '=SUM(\'Creatives KPIs\'!L2:L1000)',
    '=IF(SUM(\'Creatives KPIs\'!L2:L1000)>0;SUM(\'Creatives KPIs\'!K2:K1000)/SUM(\'Creatives KPIs\'!L2:L1000);0)',
    '=IF(SUM(\'Creatives KPIs\'!K2:K1000)>0;SUM(\'Creatives KPIs\'!O2:O1000)/SUM(\'Creatives KPIs\'!K2:K1000);0)'
  ];
  
  for (var i = 0; i < kpiLabels.length; i++) {
    var row = 6;
    var col = i * 2 + 1;
    dashboardSheet.getRange(row, col).setValue(kpiLabels[i]);
    dashboardSheet.getRange(row + 1, col).setFormula(kpiFormulas[i]);
    
    // Format KPI values
    if (i === 0 || i === 4) {
      // Money format for Spend and CPA
      dashboardSheet.getRange(row + 1, col).setNumberFormat('0.00 €');
    } else if (i === 5) {
      // Decimal for ROAS
      dashboardSheet.getRange(row + 1, col).setNumberFormat('0.00');
    } else {
      // Number format for others
      dashboardSheet.getRange(row + 1, col).setNumberFormat('#,##0');
    }
    
    // Add border and background to KPI boxes
    var kpiRange = dashboardSheet.getRange(row, col, 2, 1);
    kpiRange.setBorder(true, true, true, true, false, false);
    dashboardSheet.getRange(row, col).setBackground('#E8F0FE');
  }
  
  // Monatlicher Vergleich Bereich
  dashboardSheet.getRange('A10').setValue('MONATLICHER VERGLEICH');
  dashboardSheet.getRange('A10:F10').merge();
  dashboardSheet.getRange('A10').setFontSize(14).setFontWeight('bold');
  
  dashboardSheet.getRange('A12').setValue('Monat');
  dashboardSheet.getRange('B12').setValue('Spend');
  dashboardSheet.getRange('C12').setValue('Conversions');
  dashboardSheet.getRange('D12').setValue('CPA');
  dashboardSheet.getRange('E12').setValue('ROAS');
  
  // Formeln für den monatlichen Vergleich
  dashboardSheet.getRange('A13').setValue('Januar');
  dashboardSheet.getRange('A14').setValue('Februar');
  
  dashboardSheet.getRange('B13').setFormula('=SUMIFS(\'Creatives KPIs\'!K2:K1000; \'Creatives KPIs\'!A2:A1000; "Januar")').setNumberFormat('0.00 €');
  dashboardSheet.getRange('B14').setFormula('=SUMIFS(\'Creatives KPIs\'!K2:K1000; \'Creatives KPIs\'!A2:A1000; "Februar")').setNumberFormat('0.00 €');
  
  dashboardSheet.getRange('C13').setFormula('=SUMIFS(\'Creatives KPIs\'!L2:L1000; \'Creatives KPIs\'!A2:A1000; "Januar")').setNumberFormat('#,##0');
  dashboardSheet.getRange('C14').setFormula('=SUMIFS(\'Creatives KPIs\'!L2:L1000; \'Creatives KPIs\'!A2:A1000; "Februar")').setNumberFormat('#,##0');
  
  dashboardSheet.getRange('D13').setFormula('=IF(C13>0;B13/C13;0)').setNumberFormat('0.00 €');
  dashboardSheet.getRange('D14').setFormula('=IF(C14>0;B14/C14;0)').setNumberFormat('0.00 €');
  
  dashboardSheet.getRange('E13').setFormula('=SUMIFS(\'Creatives KPIs\'!O2:O1000; \'Creatives KPIs\'!A2:A1000; "Januar")/B13').setNumberFormat('0.00');
  dashboardSheet.getRange('E14').setFormula('=SUMIFS(\'Creatives KPIs\'!O2:O1000; \'Creatives KPIs\'!A2:A1000; "Februar")/B14').setNumberFormat('0.00');
  
  // Formatierung
  dashboardSheet.getRange('A12:E12').setBackground('#E8F0FE').setFontWeight('bold');
  
  // Kanal-Performance
  dashboardSheet.getRange('A17').setValue('KANAL-PERFORMANCE');
  dashboardSheet.getRange('A17:F17').merge();
  dashboardSheet.getRange('A17').setFontSize(14).setFontWeight('bold');
  
  dashboardSheet.getRange('A19').setValue('Kanal');
  dashboardSheet.getRange('B19').setValue('Spend');
  dashboardSheet.getRange('C19').setValue('Conversions');
  dashboardSheet.getRange('D19').setValue('CPA');
  dashboardSheet.getRange('E19').setValue('ROAS');
  
  var channels = ['Facebook', 'Instagram', 'Google', 'TikTok', 'Andere'];
  
  for (var j = 0; j < channels.length; j++) {
    dashboardSheet.getRange(20 + j, 1).setValue(channels[j]);
    
    dashboardSheet.getRange(20 + j, 2).setFormula('=SUMIFS(\'Creatives KPIs\'!K2:K1000; \'Creatives KPIs\'!B2:B1000; "' + channels[j] + '")').setNumberFormat('0.00 €');
    dashboardSheet.getRange(20 + j, 3).setFormula('=SUMIFS(\'Creatives KPIs\'!L2:L1000; \'Creatives KPIs\'!B2:B1000; "' + channels[j] + '")').setNumberFormat('#,##0');
    dashboardSheet.getRange(20 + j, 4).setFormula('=IF(C' + (20 + j) + '>0;B' + (20 + j) + '/C' + (20 + j) + ';0)').setNumberFormat('0.00 €');
    dashboardSheet.getRange(20 + j, 5).setFormula('=IF(B' + (20 + j) + '>0;SUMIFS(\'Creatives KPIs\'!O2:O1000; \'Creatives KPIs\'!B2:B1000; "' + channels[j] + '")/B' + (20 + j) + ';0)').setNumberFormat('0.00');
  }
  
  dashboardSheet.getRange('A19:E19').setBackground('#E8F0FE').setFontWeight('bold');
}

/**
 * Fügt Datenvalidierung für die Monats- und Kanalfelder hinzu
 */
function addDataValidation(ss) {
  var creativeSheet = ss.getSheetByName('Creatives KPIs');
  var adSetsSheet = ss.getSheetByName('Ad Sets KPIs');
  
  // Monatsvalidierung
  var months = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  var monthRule = SpreadsheetApp.newDataValidation().requireValueInList(months).build();
  creativeSheet.getRange('A2:A1000').setDataValidation(monthRule);
  adSetsSheet.getRange('A2:A1000').setDataValidation(monthRule);
  
  // Kanalvalidierung
  var channels = ['Facebook', 'Instagram', 'Google', 'YouTube', 'TikTok', 'Andere'];
  var channelRule = SpreadsheetApp.newDataValidation().requireValueInList(channels).build();
  creativeSheet.getRange('B2:B1000').setDataValidation(channelRule);
  adSetsSheet.getRange('B2:B1000').setDataValidation(channelRule);
}

/**
 * Wendet bedingte Formatierung an
 */
function applyConditionalFormatting(ss) {
  var creativesSheet = ss.getSheetByName('Creatives KPIs');
  var adSetsSheet = ss.getSheetByName('Ad Sets KPIs');
  
  // Bedingte Formatierung für ROAS
  var roasRange = creativesSheet.getRange('N2:N1000');
  
  // ROAS > 3 = Grün
  var goodRule = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberGreaterThan(3)
    .setBackground('#B7E1CD')
    .setRanges([roasRange])
    .build();
  
  // ROAS zwischen 2-3 = Gelb
  var mediumRule = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberBetween(2, 3)
    .setBackground('#FFF2CC')
    .setRanges([roasRange])
    .build();
  
  // ROAS < 2 = Rot
  var badRule = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberLessThan(2)
    .setBackground('#F4CCCC')
    .setRanges([roasRange])
    .build();
  
  var rules = creativesSheet.getConditionalFormatRules();
  rules.push(goodRule);
  rules.push(mediumRule);
  rules.push(badRule);
  creativesSheet.setConditionalFormatRules(rules);
  
  // Ähnliche Regeln für Ad Sets
  var adSetsRoasRange = adSetsSheet.getRange('O2:O1000');
  
  var adSetsRules = adSetsSheet.getConditionalFormatRules();
  adSetsRules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenNumberGreaterThan(3)
    .setBackground('#B7E1CD')
    .setRanges([adSetsRoasRange])
    .build());
  
  adSetsRules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenNumberBetween(2, 3)
    .setBackground('#FFF2CC')
    .setRanges([adSetsRoasRange])
    .build());
  
  adSetsRules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenNumberLessThan(2)
    .setBackground('#F4CCCC')
    .setRanges([adSetsRoasRange])
    .build());
  
  adSetsSheet.setConditionalFormatRules(adSetsRules);
}