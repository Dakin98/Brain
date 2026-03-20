/**
 * Script to set up the Razeco Performance Dashboard
 */
function setupDashboard() {
  var spreadsheetId = '19s3l4JgQz5U6jw3lgvO9LHlKGvDdzQPpEKMeteqnUqY';
  var ss = SpreadsheetApp.openById(spreadsheetId);
  
  // Rename the first sheet
  var sheet1 = ss.getSheets()[0];
  sheet1.setName('Creatives KPIs');
  
  // Create the Ad Sets KPIs sheet
  var adSetsSheet = ss.insertSheet('Ad Sets KPIs');
  
  // Set up headers for Ad Sets sheet
  var adSetsHeaders = [
    'Monat', 'Kanal', 'Kampagne', 'Ad Set ID', 'Ad Set Name', 
    'Targeting', 'Budget', 'Impressions', 'Clicks', 'CTR', 'CPC',
    'Spend', 'Conversions', 'CPA', 'ROAS', 'Umsatz'
  ];
  adSetsSheet.getRange(1, 1, 1, adSetsHeaders.length).setValues([adSetsHeaders]);
  
  // Create Dashboard sheet
  var dashboardSheet = ss.insertSheet('Dashboard');
  
  // Create Schedule sheet
  var scheduleSheet = ss.insertSheet('Update Schedule');
  var scheduleHeaders = ['Datenquelle', 'Letzte Aktualisierung', 'Nächste Aktualisierung', 'Verantwortlicher', 'Status', 'Notizen'];
  scheduleSheet.getRange(1, 1, 1, scheduleHeaders.length).setValues([scheduleHeaders]);
  
  // Add data sources
  var dataSources = [
    ['Facebook Ads', new Date(), '', 'Automatisch', 'Aktiv', 'Monatlich am 1.'],
    ['Google Ads', new Date(), '', 'Automatisch', 'Aktiv', 'Monatlich am 1.'],
    ['TikTok Ads', new Date(), '', 'Automatisch', 'Aktiv', 'Monatlich am 1.'],
    ['Analytics', new Date(), '', 'Automatisch', 'Aktiv', 'Monatlich am 1.']
  ];
  scheduleSheet.getRange(2, 1, dataSources.length, scheduleHeaders.length).setValues(dataSources);
  
  // Format all headers
  var sheets = ss.getSheets();
  for (var i = 0; i < sheets.length; i++) {
    var headerRange = sheets[i].getRange(1, 1, 1, sheets[i].getLastColumn());
    headerRange.setBackground('#4285F4');
    headerRange.setFontColor('#FFFFFF');
    headerRange.setFontWeight('bold');
  }
  
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
  
  // Set up the Dashboard with charts
  setupDashboard(ss);
  
  // Add data validation for month and channels
  addDataValidation(ss);
  
  // Freeze the header rows
  creativeSheet.setFrozenRows(1);
  adSetsSheet.setFrozenRows(1);
  
  // Auto-resize columns
  for (var i = 0; i < sheets.length; i++) {
    for (var j = 1; j <= sheets[i].getLastColumn(); j++) {
      sheets[i].autoResizeColumn(j);
    }
  }
}

/**
 * Sets up the Dashboard sheet with charts and key metrics
 */
function setupDashboard(ss) {
  var dashboardSheet = ss.getSheetByName('Dashboard');
  
  // Add title
  dashboardSheet.getRange('A1').setValue('RAZECO PERFORMANCE DASHBOARD');
  dashboardSheet.getRange('A1:F1').merge();
  dashboardSheet.getRange('A1').setFontSize(18).setFontWeight('bold');
  
  // Add date
  dashboardSheet.getRange('A2').setValue('Letzte Aktualisierung:');
  dashboardSheet.getRange('B2').setValue(new Date()).setNumberFormat('dd.MM.yyyy');
  
  // Create sections
  dashboardSheet.getRange('A4').setValue('PERFORMANCE ÜBERSICHT');
  dashboardSheet.getRange('A4:F4').merge();
  dashboardSheet.getRange('A4').setFontSize(14).setFontWeight('bold');
  
  // KPI boxes
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
}

/**
 * Adds data validation for month and channel fields
 */
function addDataValidation(ss) {
  var creativeSheet = ss.getSheetByName('Creatives KPIs');
  var adSetsSheet = ss.getSheetByName('Ad Sets KPIs');
  
  // Months validation
  var months = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  var monthRule = SpreadsheetApp.newDataValidation().requireValueInList(months).build();
  creativeSheet.getRange('A2:A1000').setDataValidation(monthRule);
  adSetsSheet.getRange('A2:A1000').setDataValidation(monthRule);
  
  // Channels validation
  var channels = ['Facebook', 'Instagram', 'Google', 'YouTube', 'TikTok', 'Andere'];
  var channelRule = SpreadsheetApp.newDataValidation().requireValueInList(channels).build();
  creativeSheet.getRange('B2:B1000').setDataValidation(channelRule);
  adSetsSheet.getRange('B2:B1000').setDataValidation(channelRule);
}

// This function is not called but would be used for monthly auto-updates
function setupTrigger() {
  // Delete all existing triggers
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
  
  // Create a monthly trigger that runs on the 1st of each month
  ScriptApp.newTrigger('updateMonthlyData')
    .timeBased()
    .onMonthDay(1)
    .atHour(1)
    .create();
}

// This function would be called by the trigger to update data
function updateMonthlyData() {
  // This function would contain API calls to Facebook, Google, etc.
  // to pull in the latest data for the previous month
  
  // Update the "Last Updated" timestamp in the dashboard
  var ss = SpreadsheetApp.openById('19s3l4JgQz5U6jw3lgvO9LHlKGvDdzQPpEKMeteqnUqY');
  var dashboardSheet = ss.getSheetByName('Dashboard');
  dashboardSheet.getRange('B2').setValue(new Date()).setNumberFormat('dd.MM.yyyy');
  
  // Update the "Next Update" dates in the schedule sheet
  var scheduleSheet = ss.getSheetByName('Update Schedule');
  var lastRow = scheduleSheet.getLastRow();
  
  for (var i = 2; i <= lastRow; i++) {
    var lastUpdateCell = scheduleSheet.getRange(i, 2);
    lastUpdateCell.setValue(new Date());
    
    // Set next update to first day of next month
    var nextMonth = new Date();
    nextMonth.setMonth(nextMonth.getMonth() + 1);
    nextMonth.setDate(1); // First day of next month
    
    scheduleSheet.getRange(i, 3).setValue(nextMonth);
  }
  
  // In a real implementation, this would include:
  // 1. API calls to ad platforms
  // 2. Data processing
  // 3. Writing data to the appropriate sheets
}