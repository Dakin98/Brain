#!/usr/bin/env node
/**
 * Auto-Setup ClickUp Dashboard via Puppeteer
 * This script logs into ClickUp and creates the dashboard automatically
 * 
 * Usage: node setup-dashboard-auto.js
 * Requirements: npm install puppeteer
 */

const puppeteer = require('puppeteer');

const CLICKUP_EMAIL = process.env.CLICKUP_EMAIL || 'your-email@example.com';
const CLICKUP_PASSWORD = process.env.CLICKUP_PASSWORD || 'your-password';
const TEAM_ID = '9006104573';

(async () => {
    console.log('🚀 Starting Automated Dashboard Setup...\n');
    
    const browser = await puppeteer.launch({ 
        headless: false, // Set to true for production
        slowMo: 50,
        args: ['--window-size=1400,900']
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 1400, height: 900 });
    
    try {
        // Step 1: Login to ClickUp
        console.log('Step 1: Logging into ClickUp...');
        await page.goto('https://app.clickup.com/login');
        
        await page.waitForSelector('input[type="email"]', { timeout: 10000 });
        await page.type('input[type="email"]', CLICKUP_EMAIL);
        await page.type('input[type="password"]', CLICKUP_PASSWORD);
        await page.click('button[type="submit"]');
        
        await page.waitForNavigation({ waitUntil: 'networkidle0' });
        console.log('✅ Logged in successfully\n');
        
        // Step 2: Navigate to Dashboards
        console.log('Step 2: Navigating to Dashboards...');
        await page.goto(`https://app.clickup.com/${TEAM_ID}/home/dashboards`);
        await page.waitForTimeout(3000);
        
        // Step 3: Create New Dashboard
        console.log('Step 3: Creating Dashboard...');
        await page.click('button:has-text("New Dashboard")');
        await page.waitForTimeout(1000);
        
        // Enter dashboard name
        await page.type('input[placeholder="Dashboard name"]', '📊 Outbound Performance Dashboard');
        await page.click('button:has-text("Create")');
        await page.waitForTimeout(2000);
        
        console.log('✅ Dashboard created\n');
        
        // Step 4: Add Widget 1 - Active Campaigns
        console.log('Step 4: Adding Widget 1 - Active Campaigns...');
        await addNumberWidget(page, {
            name: '📊 Active Campaigns',
            listName: 'Campaign Overview',
            field: 'Campaign Status',
            filterValue: 'Active'
        });
        
        // Step 5: Add Widget 2 - Emails Sent
        console.log('Step 5: Adding Widget 2 - Emails Sent...');
        await addNumberWidget(page, {
            name: '📧 Emails Sent',
            listName: 'Campaign Overview',
            calculation: 'sum',
            field: 'Sent Count'
        });
        
        // Step 6: Add Widget 3 - Reply Rate Chart
        console.log('Step 6: Adding Widget 3 - Reply Rate Chart...');
        await addChartWidget(page, {
            name: '📈 Reply Rate by Campaign',
            type: 'bar',
            listName: 'Campaign Overview',
            xField: 'Campaign Name',
            yField: 'Reply Rate %'
        });
        
        // Step 7: Add Widget 4 - Hot Leads Pie
        console.log('Step 7: Adding Widget 4 - Hot Leads Pipeline...');
        await addPieWidget(page, {
            name: '🔥 Hot Leads Pipeline',
            listName: 'Hot Leads',
            groupBy: 'Lead Status'
        });
        
        // Step 8: Add Widget 5 - Pipeline Value
        console.log('Step 8: Adding Widget 5 - Pipeline Value...');
        await addNumberWidget(page, {
            name: '💰 Pipeline Value',
            listName: 'Hot Leads',
            calculation: 'sum',
            field: 'Est. Deal Value'
        });
        
        // Step 9: Add Widget 6 - Recent Replies List
        console.log('Step 9: Adding Widget 6 - Recent Replies...');
        await addListWidget(page, {
            name: '🚨 Recent Replies (Action Needed)',
            listName: 'Hot Leads',
            filter: { field: 'Lead Status', value: 'New Reply' },
            limit: 5
        });
        
        // Step 10: Add Widget 7 - Campaigns Table
        console.log('Step 10: Adding Widget 7 - Campaigns Table...');
        await addTableWidget(page, {
            name: '📊 All Campaigns Overview',
            listName: 'Campaign Overview',
            columns: ['Campaign Name', 'Status', 'Total Leads', 'Sent Count', 'Replies', 'Reply Rate %', 'Meetings']
        });
        
        console.log('\n✅ All widgets added successfully!');
        console.log('\n🎉 Dashboard setup complete!');
        console.log('\nYou can now close the browser and use your dashboard.');
        
    } catch (error) {
        console.error('\n❌ Error:', error.message);
        console.log('\nTroubleshooting:');
        console.log('1. Make sure you provided correct email/password');
        console.log('2. Check if 2FA is enabled (disable for this script)');
        console.log('3. Ensure you have permission to create dashboards');
    }
    
    // Keep browser open for manual adjustment
    // await browser.close();
})();

// Helper function to add Number widget
async function addNumberWidget(page, config) {
    await page.click('button:has-text("Add Widget")');
    await page.waitForTimeout(500);
    
    await page.click('[data-test="widget-number"]');
    await page.waitForTimeout(500);
    
    // Set name
    await page.type('input[placeholder="Widget name"]', config.name);
    
    // Select list
    await page.click('[data-test="list-selector"]');
    await page.type('[data-test="list-selector"] input', config.listName);
    await page.waitForTimeout(500);
    await page.keyboard.press('Enter');
    
    // Add filter if specified
    if (config.filterValue) {
        await page.click('button:has-text("Add Filter")');
        await page.select('select[data-test="filter-field"]', config.field);
        await page.select('select[data-test="filter-operator"]', 'is');
        await page.type('input[data-test="filter-value"]', config.filterValue);
    }
    
    // Set calculation
    if (config.calculation === 'sum') {
        await page.select('select[data-test="calculation-type"]', 'sum');
        await page.select('select[data-test="calculation-field"]', config.field);
    }
    
    await page.click('button:has-text("Save")');
    await page.waitForTimeout(1000);
    console.log(`  ✅ ${config.name}`);
}

// Helper function to add Chart widget
async function addChartWidget(page, config) {
    await page.click('button:has-text("Add Widget")');
    await page.waitForTimeout(500);
    
    await page.click(`[data-test="widget-${config.type}-chart"]`);
    await page.waitForTimeout(500);
    
    await page.type('input[placeholder="Widget name"]', config.name);
    
    // Select list
    await page.click('[data-test="list-selector"]');
    await page.type('[data-test="list-selector"] input', config.listName);
    await page.waitForTimeout(500);
    await page.keyboard.press('Enter');
    
    // Configure axes
    await page.select('select[data-test="x-axis-field"]', config.xField);
    await page.select('select[data-test="y-axis-aggregation"]', 'average');
    await page.select('select[data-test="y-axis-field"]', config.yField);
    
    await page.click('button:has-text("Save")');
    await page.waitForTimeout(1000);
    console.log(`  ✅ ${config.name}`);
}

// Helper function to add Pie widget
async function addPieWidget(page, config) {
    await page.click('button:has-text("Add Widget")');
    await page.waitForTimeout(500);
    
    await page.click('[data-test="widget-pie-chart"]');
    await page.waitForTimeout(500);
    
    await page.type('input[placeholder="Widget name"]', config.name);
    
    // Select list
    await page.click('[data-test="list-selector"]');
    await page.type('[data-test="list-selector"] input', config.listName);
    await page.waitForTimeout(500);
    await page.keyboard.press('Enter');
    
    // Group by
    await page.select('select[data-test="group-by-field"]', config.groupBy);
    
    await page.click('button:has-text("Save")');
    await page.waitForTimeout(1000);
    console.log(`  ✅ ${config.name}`);
}

// Helper function to add List widget
async function addListWidget(page, config) {
    await page.click('button:has-text("Add Widget")');
    await page.waitForTimeout(500);
    
    await page.click('[data-test="widget-list"]');
    await page.waitForTimeout(500);
    
    await page.type('input[placeholder="Widget name"]', config.name);
    
    // Select list
    await page.click('[data-test="list-selector"]');
    await page.type('[data-test="list-selector"] input', config.listName);
    await page.waitForTimeout(500);
    await page.keyboard.press('Enter');
    
    // Add filter
    if (config.filter) {
        await page.click('button:has-text("Add Filter")');
        await page.select('select[data-test="filter-field"]', config.filter.field);
        await page.select('select[data-test="filter-operator"]', 'is');
        await page.type('input[data-test="filter-value"]', config.filter.value);
    }
    
    // Set limit
    await page.type('input[data-test="limit-input"]', config.limit.toString());
    
    await page.click('button:has-text("Save")');
    await page.waitForTimeout(1000);
    console.log(`  ✅ ${config.name}`);
}

// Helper function to add Table widget
async function addTableWidget(page, config) {
    await page.click('button:has-text("Add Widget")');
    await page.waitForTimeout(500);
    
    await page.click('[data-test="widget-table"]');
    await page.waitForTimeout(500);
    
    await page.type('input[placeholder="Widget name"]', config.name);
    
    // Select list
    await page.click('[data-test="list-selector"]');
    await page.type('[data-test="list-selector"] input', config.listName);
    await page.waitForTimeout(500);
    await page.keyboard.press('Enter');
    
    // Select columns
    for (const column of config.columns) {
        await page.click(`[data-test="column-${column}"]`);
    }
    
    await page.click('button:has-text("Save")');
    await page.waitForTimeout(1000);
    console.log(`  ✅ ${config.name}`);
}

console.log('Note: This script requires puppeteer. Install with: npm install puppeteer');
console.log('\nSet environment variables:');
console.log('  export CLICKUP_EMAIL=your@email.com');
console.log('  export CLICKUP_PASSWORD=yourpassword');
