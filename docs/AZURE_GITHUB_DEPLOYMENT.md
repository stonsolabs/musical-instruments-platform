# Azure Functions GitHub Deployment Configuration

## 🎯 **The Issue: Backend Folder Structure**

Your repository structure:
```
musical-instruments-platform/
├── backend/           # ← Azure Functions needs THIS folder
│   ├── function_app.py
│   ├── host.json
│   ├── requirements.txt
│   └── app/
├── frontend/
└── crawler/
```

Azure needs to know to deploy from `/backend` folder, not the root.

## ✅ **Solution: Configure Deployment Path**

### **Option 1: Azure Portal Deployment Center (Recommended)**

1. **Go to Azure Portal** → Your Function App → **Deployment Center**
2. **Choose GitHub** as source
3. **Authenticate** with GitHub
4. **Configure**:
   - **Repository**: `musical-instruments-platform`
   - **Branch**: `main`
   - **Build Provider**: **App Service Build Service**
   - **🔥 IMPORTANT**: Set **App location** to `/backend`

### **Option 2: Manual Configuration**

If the UI doesn't show "App location", add these settings:

**In Azure Portal → Function App → Configuration → Application Settings:**
```
SCM_BUILD_ARGS=--backend
PROJECT_DEFAULT_FUNC_APP_ROOT=backend
```

## 🛠️ **Step-by-Step Setup**

### **1. In Azure Portal:**
```
Function App → Deployment Center → Settings

Source: GitHub
Repository: your-username/musical-instruments-platform
Branch: main
Build Provider: App Service Build Service (Kudu)
App location: backend    ← KEY SETTING
```

### **2. Verify Configuration:**
After setup, check these settings exist:
```
Configuration → Application Settings:
- WEBSITE_RUN_FROM_PACKAGE: 1
- PROJECT_DEFAULT_FUNC_APP_ROOT: backend
```

### **3. Test Deployment:**
Make a small change in `/backend` folder and push:
```bash
# Make a small change to test
echo "# Test deployment" >> backend/README.md
git add backend/README.md
git commit -m "Test Azure Functions deployment from backend folder"
git push origin main
```

## 📁 **Alternative: Repository Structure**

### **If Folder Detection Doesn't Work:**

**Option A: Add .deployment File**
Create `/backend/.deployment`:
```ini
[config]
project = .
```

**Option B: Use GitHub Actions (More Control)**
Create `.github/workflows/azure-functions-deploy.yml`:
```yaml
name: Deploy Azure Functions

on:
  push:
    branches: [ main ]
    paths: [ 'backend/**' ]  # Only trigger on backend changes

jobs:
  deploy:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./backend  # Work in backend folder

    steps:
    - uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt --target=".python_packages/lib/site-packages"

    - name: Deploy to Azure Functions
      uses: Azure/functions-action@v1
      with:
        app-name: 'getyourmusicgear-backend'
        package: './backend'
        publish-profile: ${{ secrets.AZUREAPPSERVICE_PUBLISHPROFILE }}
```

## 🔍 **Verify Deployment Success**

### **Check Deployment Logs:**
1. **Azure Portal** → Function App → **Deployment Center** → **Logs**
2. Look for successful build messages
3. Verify it's building from `/backend` folder

### **Test Endpoints:**
```bash
# Test health endpoint
curl https://getyourmusicgear-backend.azurewebsites.net/health

# Test API endpoint (with your API key)
curl -H "X-API-Key: your-api-key" \
  https://getyourmusicgear-backend.azurewebsites.net/api/v1/products?limit=1
```

## ⚠️ **Common Issues & Solutions**

### **Issue 1: "No Function Found"**
**Problem**: Azure didn't find `function_app.py`
**Solution**: Ensure `PROJECT_DEFAULT_FUNC_APP_ROOT=backend` is set

### **Issue 2: "Module Not Found"**  
**Problem**: Python packages not installing correctly
**Solution**: Check `requirements.txt` is in `/backend` folder

### **Issue 3: "Build Failed"**
**Problem**: Wrong folder being built
**Solution**: Verify **App location** is set to `backend`

## 📊 **Deployment Workflow**

### **What Happens When You Push:**
1. **GitHub webhook** triggers Azure deployment
2. **Azure detects** changes in repository
3. **Builds from** `/backend` folder (because of your configuration)
4. **Installs** Python packages from `/backend/requirements.txt`
5. **Deploys** `function_app.py` and `/backend/app` folder
6. **Function App** becomes available with your API

### **Files Azure Uses:**
```
backend/
├── function_app.py      # ← Entry point
├── host.json           # ← Azure Functions config
├── requirements.txt    # ← Dependencies to install
├── local.settings.json # ← Ignored (for local dev only)
└── app/               # ← Your FastAPI application
```

## 🎯 **Key Configuration Summary**

**Essential Settings for Backend Folder Deployment:**
1. **App location**: `backend` (in Deployment Center)
2. **PROJECT_DEFAULT_FUNC_APP_ROOT**: `backend` (Application Settings)
3. **Repository**: `your-username/musical-instruments-platform`
4. **Branch**: `main`

**With these settings, Azure will:**
✅ Monitor only `/backend` folder for changes
✅ Build from `/backend` as the root  
✅ Install packages from `/backend/requirements.txt`
✅ Deploy your FastAPI app correctly

Your automatic deployment will work perfectly once you specify the `/backend` folder path! 🚀