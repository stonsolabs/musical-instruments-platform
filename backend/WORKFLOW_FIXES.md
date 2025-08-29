# GitHub Actions Workflow Fixes

## Issues with Current Workflow

Your current workflow had several issues that caused the deployment failures:

### ❌ **Issues Found:**

1. **Missing dependency target path**:
   ```yaml
   pip install -r requirements.txt  # ❌ Wrong - dependencies not in right place
   ```
   Should be:
   ```yaml
   pip install -r requirements.txt --target=".python_packages/lib/site-packages"
   ```

2. **Virtual environment not activated**:
   ```yaml
   python -m venv venv
   source venv/bin/activate  # ❌ Not used in subsequent steps
   ```

3. **Incorrect deployment package**:
   ```yaml
   package: '.'  # ❌ Wrong - trying to deploy unzipped directory
   ```
   Should be:
   ```yaml
   package: './release.zip'  # ✅ Deploy ZIP file directly
   ```

4. **No cleanup of development files**:
   - `venv/`, `__pycache__/`, `.env*` files were being included

5. **No path-based trigger**:
   - Workflow triggers on ANY change, not just backend changes

6. **Malformed publish profile reference**:
   ```yaml
   publish-profile: ${{ secrets.AZUREAPPSERVICE_PUBLISHPROFILE_675C49512C594314BAAACAA9F6D5FD95 }}main_getyourmusicgear-backend.yml
   ```
   The filename got appended by mistake.

## ✅ **Fixed Version:**

The corrected workflow (`main_getyourmusicgear-backend_FIXED.yml`) includes:

1. **Proper dependency installation**
2. **Clean up of development files**  
3. **Path-based triggers** (only runs on backend changes)
4. **Correct ZIP deployment**
5. **Better error handling and verification**
6. **Fixed publish profile reference**

## 🚀 **How to Apply the Fix:**

1. **Replace your current workflow**:
   ```bash
   # Copy the fixed workflow to your .github/workflows/ directory
   cp backend/main_getyourmusicgear-backend_FIXED.yml .github/workflows/main_getyourmusicgear-backend.yml
   ```

2. **Commit and push**:
   ```bash
   git add .github/workflows/main_getyourmusicgear-backend.yml
   git commit -m "Fix Azure Functions deployment workflow"
   git push origin main
   ```

## 🔧 **Key Improvements:**

### Before (Problematic):
```yaml
- name: Install dependencies
  run: |
    cd backend
    pip install -r requirements.txt

- name: Zip artifact for deployment
  run: |
    cd backend
    zip -r ../release.zip ./*

- name: 'Deploy to Azure Functions'
  with:
    package: '.'  # ❌ Wrong package reference
```

### After (Fixed):
```yaml
- name: Install dependencies with proper target
  run: |
    source venv/bin/activate
    cd backend
    pip install -r requirements.txt --target=".python_packages/lib/site-packages"

- name: Clean up development files
  run: |
    cd backend
    rm -rf venv/ __pycache__/ .pytest_cache/ .coverage *.pyc
    rm -f local.settings.json .env*

- name: Zip artifact for deployment
  run: |
    cd backend
    zip -r ../release.zip . -x "venv/*" "__pycache__/*" "*.pyc" ".env*" "local.settings.json"

- name: 'Deploy to Azure Functions'
  with:
    package: './release.zip'  # ✅ Correct ZIP package
    scm-do-build-during-deployment: true
```

## 🧪 **Testing the Fix:**

After applying the fix, the workflow will:

1. ✅ Only trigger on backend changes
2. ✅ Install dependencies in the correct location
3. ✅ Clean up unnecessary files
4. ✅ Create a proper deployment package
5. ✅ Deploy successfully to Azure Functions
6. ✅ Verify the deployment with a health check

## 📋 **Final Steps:**

1. Update your workflow file with the fixed version
2. Make a small change to the backend (like updating a comment)
3. Push to trigger the workflow
4. Monitor the GitHub Actions run to confirm it works
5. Test your deployed function at: `https://getyourmusicgear-backend.azurewebsites.net/health`

The deployment should now complete successfully without the "From directory doesn't exist" error!