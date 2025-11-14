# Acoustic Guardian - Bill of Materials (BOM)

## Core Components

| Component | Quantity | Unit Cost (USD) | Total Cost (USD) | Supplier | Notes |
|-----------|----------|-----------------|------------------|----------|-------|
| TTGO T-Call ESP32 SIM800L | 1 | $12.99 | $12.99 | Amazon, AliExpress | Integrated GSM module |
| INMP441 I2S MEMS Microphone | 1 | $3.99 | $3.99 | Amazon, AliExpress | Digital microphone |
| MicroSD Card (32GB) | 1 | $4.99 | $4.99 | Amazon, eBay | For firmware updates |
| SIM Card with Data Plan | 1 | $5.00/month | $5.00/month | Local carrier | Check coverage in deployment area |

## Power System

| Component | Quantity | Unit Cost (USD) | Total Cost (USD) | Supplier | Notes |
|-----------|----------|-----------------|------------------|----------|-------|
| Solar Panel (10W) | 1 | $14.99 | $14.99 | Amazon, Adafruit | Monocrystalline recommended |
| Li-ion Battery (3.7V 2000mAh) | 1 | $6.99 | $6.99 | Amazon, AliExpress | Protected variant |
| Charge Controller (TP4056) | 1 | $1.99 | $1.99 | Amazon, AliExpress | With protection circuit |
| DC-DC Boost Converter (3.7V to 5V) | 1 | $2.99 | $2.99 | Amazon, AliExpress | MT3608 recommended |

## Enclosure & Protection

| Component | Quantity | Unit Cost (USD) | Total Cost (USD) | Supplier | Notes |
|-----------|----------|-----------------|------------------|----------|-------|
| IP65 Waterproof Enclosure | 1 | $9.99 | $9.99 | Amazon, AliExpress | 150mm x 100mm x 75mm |
| Cable Glands (PG7-PG9) | 4 | $2.50 | $10.00 | Amazon, electrical suppliers | For waterproof cable entry |
| Heat Shrink Tubing Kit | 1 | $5.99 | $5.99 | Amazon, electronics stores | Various sizes |
| Terminal Block (5-position) | 1 | $2.99 | $2.99 | Amazon, electronics stores | For wire connections |

## Installation Hardware

| Component | Quantity | Unit Cost (USD) | Total Cost (USD) | Supplier | Notes |
|-----------|----------|-----------------|------------------|----------|-------|
| Galvanized Steel Pole (2m) | 1 | $25.00 | $25.00 | Hardware store | 1.5" diameter recommended |
| Concrete Mix | 1 | $5.00 | $5.00 | Hardware store | For pole foundation |
| U-Bolts & Clamps | 2 | $3.99 | $7.98 | Hardware store | For device attachment |
| Stainless Steel Screws | 1 pack | $4.99 | $4.99 | Hardware store | Various lengths |

## Tools & Consumables

| Component | Quantity | Unit Cost (USD) | Total Cost (USD) | Supplier | Notes |
|-----------|----------|-----------------|------------------|----------|-------|
| Crimping Tool | 1 | $15.00 | $15.00 | Hardware store | For cable glands |
| Wire Strippers | 1 | $8.99 | $8.99 | Hardware store | Multi-gauge |
| Multimeter | 1 | $19.99 | $19.99 | Amazon, electronics stores | Basic digital model |
| Jumper Wires (Male-Female) | 10 | $2.99 | $2.99 | Amazon, electronics stores | For prototyping |
| Soldering Iron Kit | 1 | $24.99 | $24.99 | Amazon, electronics stores | With stand and accessories |

## Software & Services

| Component | Quantity | Unit Cost (USD) | Total Cost (USD) | Supplier | Notes |
|-----------|----------|-----------------|------------------|----------|-------|
| Edge Impulse Subscription | 1 | $0-$499/month | $0-$499/month | Edge Impulse | Free tier available |
| InfluxDB Cloud Subscription | 1 | $0-$200/month | $0-$200/month | InfluxData | Free tier available |
| Grafana Cloud Subscription | 1 | $0-$499/month | $0-$499/month | Grafana Labs | Free tier available |

## Estimated Total Costs

### One-time Hardware Costs
- **Basic Components**: ~$120.90
- **Tools & Equipment**: ~$76.95
- **Total Initial Investment**: ~$197.85

### Monthly Operating Costs
- **SIM Card Data Plan**: $5.00
- **Cloud Services**: $0 (using free tiers)
- **Total Monthly Cost**: $5.00

### Scaling Costs
For each additional deployment node:
- **Hardware**: ~$120.90
- **Installation**: Variable (professional installation ~$100-200)

## Alternative Suppliers

### Budget Options
- **Banggood**: Often cheaper than Amazon but longer shipping times
- **AliExpress**: Good for bulk orders but 2-4 weeks delivery
- **Local Electronics Stores**: Faster availability but possibly higher prices

### Premium Options
- **Adafruit**: Higher quality components with excellent documentation
- **SparkFun**: Educational resources and reliable products
- **Digi-Key/Mouser**: Professional grade components with same-day shipping

## Procurement Tips

### Bulk Purchasing
- Order microphones and ESP32 boards in quantities of 10+ for discounts
- Buy batteries from the same batch for consistent performance
- Purchase cable glands in packs of 10 for future projects

### Quality Assurance
- Verify ESP32 boards have genuine ESP32-WROVER modules
- Check microphone sensitivity specifications before purchase
- Ensure solar panels are rated for outdoor use with junction box

### Lead Times
- Standard components: 3-7 business days
- Specialized items: 2-4 weeks
- Plan procurement 4-6 weeks before deployment

## Regional Considerations

### Tropical Climates
- Use UV-resistant enclosures and cables
- Consider larger solar panels for cloudy conditions
- Select corrosion-resistant hardware (stainless steel)

### Arid Climates
- Ensure adequate ventilation in enclosure
- Use temperature-rated batteries (-20°C to +60°C)
- Increase cleaning frequency for dust removal

### Temperate Climates
- Standard components typically sufficient
- Seasonal considerations for solar charging
- Moderate maintenance schedule adequate

## Warranty & Support

### Component Warranties
- ESP32 boards: Typically 6 months to 1 year
- Microphones: 1 year
- Batteries: 6 months to 1 year
- Solar panels: 10-25 years (performance warranty)

### Vendor Support
- Amazon: 30-day return policy
- AliExpress: Varies by seller (15-45 days)
- Direct from manufacturer: Check individual policies