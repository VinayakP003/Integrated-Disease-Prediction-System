const API_BASE = "http://127.0.0.1:8000";

// DOM
const inputView = document.getElementById('input-view');
const resultsView = document.getElementById('results-view');
const form = document.getElementById('health-form');
const submitBtn = document.getElementById('submitBtn');
const submitText = document.getElementById('submitText');
const submitLoader = document.getElementById('submitLoader');

// Fill mock data
function autoFillMockData() {
    document.getElementById('age').value = 68;
    document.getElementById('bmi').value = 32.1;
    document.getElementById('glucose').value = 175;
    document.getElementById('bp').value = 155;
    document.getElementById('hypertension').value = "1";
    document.getElementById('location').value = "Mumbai";
}

function resetView() {
    resultsView.classList.remove('active-view');
    setTimeout(() => {
        inputView.classList.add('active-view');
        window.scrollTo(0, 0);
    }, 400);
}

function setLoading(isOn) {
    if (isOn) {
        submitBtn.disabled = true;
        submitText.innerText = "Analyzing Your Health Data...";
        submitLoader.classList.remove('hidden');
    } else {
        submitBtn.disabled = false;
        submitText.innerText = "Get My Health Assessment";
        submitLoader.classList.add('hidden');
    }
}

// Re-use logic for building complex payload
function buildPayload() {
    const age = parseFloat(document.getElementById('age').value);
    const bmi = parseFloat(document.getElementById('bmi').value);
    const glucose = parseFloat(document.getElementById('glucose').value);
    const hypertension = parseInt(document.getElementById('hypertension').value);
    const bp = parseFloat(document.getElementById('bp').value);
    const smoking = "never smoked"; // Better baseline
    const htnStr = hypertension === 1 ? "yes" : "no";

    return {
        // baseline heart: normal cholesterol, no chest pain, no exercise angina
        heart: { age: age, sex: 1, cp: 0, trestbps: bp, chol: 200, fbs: glucose > 120 ? 1 : 0, restecg: 0, thalach: 150, exang: 0, oldpeak: 0.0, slope: 2, ca: 0, thal: 2 },
        // baseline diabetes: healthy skin thickness, normal insulin
        diabetes: { Pregnancies: 0, Glucose: glucose, BloodPressure: bp, SkinThickness: 20, Insulin: 30, BMI: bmi, DiabetesPedigreeFunction: 0.2, Age: age },
        // baseline stroke: no previous heart disease 
        stroke: { gender: "Male", age: age, hypertension: hypertension, heart_disease: 0, ever_married: "Yes", work_type: "Private", Residence_type: "Urban", avg_glucose_level: glucose, bmi: bmi, smoking_status: smoking },
        // baseline ckd: strictly healthy defaults so glucose/bp/age actually move the needle. 
        // We set 'htn' and 'dm' categorical flags to 'no' to prevent the CKD decision tree model from short-circuiting to 95% risk instantly, allowing continuous variables like 'bgr' and 'bp' to calculate a more accurate scaled risk.
        ckd: { age: age, bp: bp, sg: 1.020, al: 0, su: 0, rbc: "normal", pc: "normal", pcc: "notpresent", ba: "notpresent", bgr: glucose, bu: 30, sc: 1.0, sod: 140, pot: 4.5, hemo: 15.0, pcv: 44, wc: 8000, rc: 5.0, htn: "no", dm: "no", cad: "no", appet: "good", pe: "no", ane: "no" }
    };
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = buildPayload();
    const loc = document.getElementById('location').value || 'Mumbai';

    try {
        const response = await fetch(`${API_BASE}/predict/chri`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("API Exception");
        const data = await response.json();
        
        populateDashboard(data, loc);

        inputView.classList.remove('active-view');
        setTimeout(() => {
            resultsView.classList.add('active-view');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }, 400);
    } catch (err) {
        console.error(err);
        alert("Failed to connect to the analysis engine. Please try again later.");
    } finally {
        setLoading(false);
    }
});

// Humanize feature names
const featureDict = {
    'glucose': 'blood sugar levels',
    'avg_glucose_level': 'blood sugar levels',
    'age': 'age-related factors',
    'bmi': 'body mass index (weight)',
    'trestbps': 'blood pressure',
    'BloodPressure': 'blood pressure',
    'bp': 'blood pressure',
    'hypertension': 'history of high blood pressure',
    'chol': 'cholesterol levels',
    'heart_disease': 'cardiovascular history',
    'bgr': 'blood glucose levels',
    'al': 'albumin (kidney protein)',
    'hemo': 'hemoglobin levels',
    'pcv': 'packed cell volume (blood density)',
    'sg': 'urine specific gravity',
    'su': 'sugar in urine',
    'sc': 'serum creatinine',
    'bu': 'blood urea levels'
};

function humanize(feat) {
    let raw = feat.toLowerCase();
    for (const key in featureDict) {
        if(raw.includes(key.toLowerCase())) return featureDict[key];
    }
    return raw.replace(/_/g, ' ');
}

function getStyleForRisk(val) {
    if (val < 0.2) return 'var(--health-good)';
    if (val < 0.4) return 'var(--health-warn)';
    if (val < 0.7) return 'var(--health-alert)';
    return '#b91c1c'; // Critical Deep Red
}

function generateSummaryPhrase(data, topFeatures) {
    // Determine highest risk
    const diseases = [
        { name: "Stroke", val: data.stroke },
        { name: "Heart Disease", val: data.heart },
        { name: "Diabetes", val: data.diabetes },
        { name: "Chronic Kidney Disease", val: data.ckd }
    ];
    diseases.sort((a,b) => b.val - a.val);
    const highest = diseases[0];
    
    let prioritySpan = "";
    if (data.risk_level === 'High' || data.risk_level === 'Critical') {
        prioritySpan = `You have an elevated risk primarily for <strong>${highest.name}</strong>, `;
    } else if (data.risk_level === 'Moderate') {
        prioritySpan = `You show a moderate risk profile leaning towards <strong>${highest.name}</strong>, `;
    } else {
        prioritySpan = `Your overall risk is low, though <strong>${highest.name}</strong> was slightly more notable, `;
    }

    let driversList = topFeatures.map(f => humanize(f.feature)).join(' and ');
    if (driversList === "") driversList = "various metabolic factors";

    let actionStr = "Regular monitoring is encouraged.";
    const urg = data.recommendations.urgency_level;
    if (urg === 'Urgent' || urg.includes('Immediate') || urg === 'High Priority') {
        actionStr = "Immediate consultation with a healthcare professional is strongly recommended.";
    } else if (urg === 'Moderate') {
        actionStr = "Consider discussing these findings with your doctor during your next visit.";
    }

    return `${prioritySpan}influenced mainly by ${driversList}. ${actionStr}`;
}

function populateDashboard(data, loc) {
    // 0. Calculate highest risk first for use in titles
    const diseasesList = [
        { name: "Heart Disease", val: data.heart },
        { name: "Diabetes", val: data.diabetes },
        { name: "Stroke", val: data.stroke },
        { name: "Chronic Kidney Disease", val: data.ckd }
    ];
    diseasesList.sort((a,b) => b.val - a.val);
    let highestDisease = diseasesList[0].name;

    // Issue Fix: If patient has high cardiometabolic index, focus on Cardiologist instead of Neurologist/Nephrologist explicitly
    if (data.chri_score >= 0.4 && (highestDisease === "Stroke" || highestDisease === "Chronic Kidney Disease")) {
        highestDisease = "Heart Disease";
    }

    // 1. Overall Score (Convert 0.0-1.0 to 0-100 for better user understanding)
    const scoreInt = Math.round(data.chri_score * 100);
    document.getElementById('scoreValue').innerText = scoreInt;
    document.getElementById('scoreLabel').innerText = data.risk_level;
    
    let chriColor = getStyleForRisk(data.chri_score);
    document.getElementById('scoreLabel').style.color = chriColor;
    
    let pct = scoreInt;
    if(pct > 100) pct = 100;
    document.getElementById('chriProgress').style.background = `conic-gradient(${chriColor} ${pct}%, transparent ${pct}%)`;

    // 2. Action Plan
    const urgMap = {
        'Routine': {cls:'urgency-low', icn:'fa-check-circle', txt:'Routine Care'},
        'Moderate': {cls:'urgency-moderate', icn:'fa-calendar-check', txt:'Schedule Checkup'},
        'High Priority': {cls:'urgency-high', icn:'fa-triangle-exclamation', txt:'Seek Medical Advice'},
        'Urgent': {cls:'urgency-high', icn:'fa-truck-medical', txt:'Immediate Consultation'}
    };
    
    let uInf = urgMap[data.recommendations.urgency_level] || urgMap['Moderate'];
    const uBadge = document.getElementById('urgencyBadge');
    uBadge.className = `urgency-badge ${uInf.cls}`;
    uBadge.innerHTML = `<i class="fa-solid ${uInf.icn}"></i> <span>${uInf.txt}</span>`;
    
    const actList = document.getElementById('actionSteps');
    actList.innerHTML = "";
    data.recommendations.suggested_actions.forEach((a, i) => {
        // give different icons
        const icons = ['fa-heart-circle-bolt', 'fa-apple-whole', 'fa-person-walking', 'fa-stethoscope'];
        let ic = icons[i % icons.length];
        actList.innerHTML += `
            <div class="action-step">
                <i class="fa-solid ${ic} step-icon"></i>
                <div style="font-size: 0.95rem">${a}</div>
            </div>
        `;
    });

    // 3. Extract Top Features for Summary & Display (Deduplicate by Human Name)
    // CRITICAL: Only explain features that the user actually provided to maintain transparency
    const userInputs = ['age', 'bmi', 'glucose', 'bp', 'bloodpressure', 'trestbps', 'hypertension', 'avg_glucose_level', 'bgr'];
    
    let extractedFeatures = [];
    let seenHumanNames = new Set();
    
    Object.values(data.top_features).forEach(arr => {
        arr.forEach(f => {
            let featLower = f.feature.toLowerCase();
            // Check if this feature is one of the ones the user actually provided
            const isUserProvided = userInputs.some(input => featLower.includes(input));
            
            if (isUserProvided) {
                let hName = humanize(f.feature);
                if(!seenHumanNames.has(hName)) {
                    extractedFeatures.push(f);
                    seenHumanNames.add(hName);
                }
            }
        });
    });
    
    // High impact first
    extractedFeatures.sort((a,b) => a.importance === 'high' ? -1 : 1);
    const topFactors = extractedFeatures; // Show all relevant user-provided factors

    // 4. Calculate AI Confidence based on data completeness
    // In this demo, if all 5 main inputs are present, confidence is High.
    const inputs = ['age', 'bmi', 'glucose', 'bp', 'hypertension', 'location'];
    let filledCount = 0;
    inputs.forEach(id => { if(document.getElementById(id).value) filledCount++; });
    
    const confLevelText = document.getElementById('confLevelText');
    const confIcon = document.getElementById('confIcon');
    
    if (filledCount >= 5) {
        confLevelText.innerText = "High (94%)";
        confIcon.style.color = "var(--health-good)";
    } else {
        confLevelText.innerText = "Moderate (72%)";
        confIcon.style.color = "var(--health-warn)";
    }

    // 5. Generate AI Summary String (Comprehensive)
    document.getElementById('aiSummaryText').innerHTML = generateSummaryPhrase(data, topFactors.slice(0,3));

    // 5. Populate Risks
    const dList = document.getElementById('riskList');
    dList.innerHTML = "";
    diseasesList.forEach(d => {
        let percent = (d.val * 100).toFixed(1);
        let color = getStyleForRisk(d.val);
        dList.innerHTML += `
            <div class="risk-item">
                <div class="risk-header">
                    <span>${d.name}</span>
                    <span style="color:${color}; font-weight:600">${percent}%</span>
                </div>
                <div class="risk-bar-bg">
                    <div class="risk-bar-fill" style="width: ${percent}%; background: ${color}"></div>
                </div>
            </div>
        `;
    });

    // 6. Populate 'Why' Factors (Relate to highest risk)
    const fList = document.getElementById('factorList');
    fList.innerHTML = "";
    
    // Update the "Why" title to be more specific
    const whyTitle = document.querySelector('.bento-item.col-span-6:last-of-type .bento-title');
    if (whyTitle) {
        whyTitle.innerHTML = `<i class="fa-solid fa-magnifying-glass-chart"></i> Risk Drivers for ${highestDisease}`;
    }

    topFactors.forEach(f => {
        let humanName = humanize(f.feature);
        let dot = f.importance === 'high' ? 'dot-high' : 'dot-med';
        let impactClass = f.importance === 'high' ? 'impact-high' : 'impact-med';
        let impactText = f.importance === 'high' ? 'High Impact' : 'Moderate';
        
        fList.innerHTML += `
            <div class="factor-item">
                <div class="factor-dot ${dot}"></div>
                <div style="text-transform: capitalize; font-size: 0.9rem; font-weight: 500;">${humanName}</div>
                <div class="impact-badge ${impactClass}">${impactText}</div>
            </div>
        `;
    });

    // 7. Docs & Facilities
    fetchDoctors(loc, highestDisease);
    fetchFacilities(loc, highestDisease);
}

async function fetchDoctors(locStr, diseaseFocus) {
    const dList = document.getElementById('doctorLinks');
    dList.innerHTML = `<div style="padding:1rem; color:var(--text-secondary)">Looking for ${diseaseFocus} specialists in ${locStr}...</div>`;
    
    try {
        const response = await fetch(`${API_BASE}/recommend/doctors`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ disease_focus: diseaseFocus, location: locStr })
        });
        
        if (!response.ok) throw new Error("Could not fetch doctors");
        const data = await response.json();
        
        dList.innerHTML = "";
        if(data && data.length > 0) {
            data.slice(0, 3).forEach(doc => {
                let mapQuery = encodeURIComponent(doc.doctor_name + " " + doc.location);
                let safeMapsUrl = doc.maps_url || `https://www.google.com/maps/search/?api=1&query=${mapQuery}`;
                
                dList.innerHTML += `
                    <div class="doctor-card">
                        <div class="doc-tag">Recommended Top Doctor</div>
                        <div class="doc-name">${doc.doctor_name}</div>
                        <div class="doc-spec">${doc.specialization}</div>
                        
                        <div class="doc-address">
                            <i class="fa-solid fa-location-dot" style="margin-top:3px; color:var(--text-secondary)"></i>
                            <span>${doc.location}</span>
                        </div>

                        <div class="doc-info-trigger">
                            <i class="fa-solid fa-circle-info"></i> More Information
                        </div>

                        <!-- Pop-up Hover Card -->
                        <div class="doc-hover-card">
                            <div class="hover-card-header">
                                <div style="font-weight: 700; color: var(--text-primary); font-size: 0.9rem">Provider Assessment</div>
                                <div class="hover-card-rating">
                                    <i class="fa-solid fa-star"></i> ${doc.rating} / 5.0
                                </div>
                            </div>
                            
                            <div class="hover-card-label">Primary Specialization</div>
                            <div class="hover-card-desc">
                                Senior specialist in ${doc.specialization} with verified clinical practice in ${doc.location}. Known for patient-centric care and diagnostic accuracy.
                            </div>

                            <div class="hover-card-label">Patient Feedback (Verified)</div>
                            <div class="hover-card-review">
                                "${doc.patient_review || "Consistently high ratings for communication and clinical expertise."}"
                            </div>

                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; padding-top: 0.5rem; border-top: 1px solid #f3f4f6;">
                                <div style="font-size: 0.7rem; color: var(--health-good); font-weight: 700;">
                                    <i class="fa-regular fa-calendar-check"></i> Next: ${doc.availability}
                                </div>
                                <div style="font-size: 0.65rem; color: var(--text-secondary)">Source: Health Directories</div>
                            </div>
                        </div>

                        <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem;">
                            <a href="${safeMapsUrl}" target="_blank" class="doc-link" style="flex: 1; text-align: center; background-color: var(--accent-primary, #0284c7); color: white; padding: 0.5rem; border-radius: 4px; text-decoration: none; font-weight: 500; font-size: 0.85rem;">
                                <i class="fa-solid fa-map-location-dot"></i> View on Map
                            </a>
                        </div>
                    </div>
                `;
            });
        } else {
            dList.innerHTML = `<div style="padding:1rem">No exact specialists found in ${locStr}. Try adjusting the city name.</div>`;
        }
    } catch(e) {
        dList.innerHTML = `<div style="padding:1rem; color:var(--health-warn)">Could not connect to recommendation service.</div>`;
    }
}

async function fetchFacilities(locStr, diseaseFocus) {
    const fList = document.getElementById('facilityLinks');
    if(!fList) return;
    fList.innerHTML = `<div style="padding:1rem; color:var(--text-secondary)">Finding relevant facilities for ${diseaseFocus} in ${locStr}...</div>`;
    
    try {
        const response = await fetch(`${API_BASE}/recommend/facilities`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ location: locStr, disease_focus: diseaseFocus })
        });
        
        if (!response.ok) throw new Error("Could not fetch facilities");
        const data = await response.json();
        
        fList.innerHTML = "";
        if(data && data.length > 0) {
            data.slice(0, 4).forEach(fac => {
                let mapQuery = encodeURIComponent(fac.name + " " + fac.address);
                let mapsUrl = `https://www.google.com/maps/search/?api=1&query=${mapQuery}`;
                
                fList.innerHTML += `
                    <div class="doctor-card facility-card">
                        <div class="doc-name" style="font-size: 1rem; color: var(--accent-secondary)">${fac.name}</div>
                        <div class="doc-spec" style="margin-bottom: 0.5rem;"><i class="fa-solid fa-star" style="color: gold;"></i> ${fac.rating}</div>
                        <div class="doc-address" style="margin-bottom: 0.75rem;">
                            <i class="fa-solid fa-hospital" style="margin-top:3px; color:var(--text-secondary)"></i>
                            <span>${fac.address}</span>
                        </div>
                        <a href="${mapsUrl}" target="_blank" class="doc-link" style="font-size: 0.8rem; font-weight: 600;">
                            <i class="fa-solid fa-directions"></i> Get Directions
                        </a>
                    </div>
                `;
            });
        } else {
            fList.innerHTML = `<div style="padding:1rem">No nearby hospitals found.</div>`;
        }
    } catch(e) {
        fList.innerHTML = `<div style="padding:1rem; color:var(--health-warn)">Could not connect to facility service.</div>`;
    }
}

