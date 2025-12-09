# Hướng dẫn Sử dụng Hệ thống Đánh giá và Kiểm tra Dự án

## Mục đích

Hệ thống này giúp bạn:
1. Đánh giá tỷ lệ hoàn thiện dự án
2. Đối chiếu lý thuyết với thực tế
3. Kiểm tra chất lượng và tuân thủ tiêu chuẩn
4. Tự động hóa quy trình review và báo cáo

---

## 1. Cấu trúc Hệ thống

```
.
├── docs/
│   ├── theory/
│   │   └── THEORY.md              # Tài liệu lý thuyết và quy trình
│   ├── checklists/
│   │   ├── CHECKLIST.md           # Danh sách kiểm tra hoàn thiện
│   │   └── STANDARDS.md           # Tiêu chuẩn đánh giá
│   ├── templates/
│   │   └── REPORT_TEMPLATE.md     # Template báo cáo
│   └── reports/                   # Thư mục lưu báo cáo
├── scripts/
│   ├── calculate_completion.py    # Script tính tỷ lệ hoàn thiện
│   └── cross_reference.py         # Script đối chiếu lý thuyết/thực tế
└── .github/
    ├── workflows/
    │   └── project_review.yml     # GitHub Actions workflow
    └── ISSUE_TEMPLATE/
        ├── completion-item.md     # Template issue cho items chưa hoàn thành
        └── quality-issue.md       # Template issue cho vấn đề chất lượng
```

---

## 2. Quy trình Sử dụng

### Bước 1: Làm quen với Tài liệu Lý thuyết

Đọc và hiểu các tài liệu cơ bản:

```bash
# Đọc tài liệu lý thuyết
cat docs/theory/THEORY.md

# Đọc checklist
cat docs/checklists/CHECKLIST.md

# Đọc tiêu chuẩn
cat docs/checklists/STANDARDS.md
```

### Bước 2: Đánh giá Tỷ lệ Hoàn thiện

#### 2.1 Cập nhật Checklist

Mở file `docs/checklists/CHECKLIST.md` và đánh dấu các items đã hoàn thành:

```markdown
# Chưa hoàn thành
- [ ] Item chưa làm

# Đã hoàn thành
- [x] Item đã làm xong
```

#### 2.2 Chạy Script Tính Toán

```bash
# Chạy script để tính tỷ lệ hoàn thiện
python3 scripts/calculate_completion.py

# Hoặc chỉ định file checklist cụ thể
python3 scripts/calculate_completion.py docs/checklists/CHECKLIST.md
```

**Output:**
```
======================================================================
BÁO CÁO TỶ LỆ HOÀN THIỆN DỰ ÁN
======================================================================

File phân tích: docs/checklists/CHECKLIST.md

Tổng số items: 100
Items đã hoàn thành: 75
Items còn lại: 25

Tỷ lệ hoàn thiện: 75.00%
Trạng thái: 🟠 Đã phát triển cơ bản

======================================================================
ĐỀ XUẤT HÀNH ĐỘNG:
✓ Ưu tiên phát triển các features quan trọng còn thiếu
✓ Thiết lập CI/CD nếu chưa có
======================================================================
```

### Bước 3: Đối chiếu Lý thuyết với Thực tế

Chạy script phân tích dự án:

```bash
python3 scripts/cross_reference.py
```

Script này sẽ:
- Quét cấu trúc dự án
- Phát hiện các components (backend, frontend, database, etc.)
- Đánh giá tính đầy đủ của các thành phần
- Tạo báo cáo JSON

**Output:**
```
======================================================================
BÁO CÁO ĐỐI CHIẾU LÝ THUYẾT VỚI THỰC TẾ
======================================================================

📁 CẤU TRÚC DỰ ÁN:
  Backend: ✅
  Frontend: ✅
  Database: ❌
  Tests: ✅
  Documentation: ✅
  DevOps: ❌

🔧 BACKEND:
  Số file backend: 25
  API structure: ✅
  Authentication: ✅
  Data models: ✅

[...]

📊 TỔNG KẾT:
  Tổng số kiểm tra: 20
  Số kiểm tra đạt: 15
  Tỷ lệ đạt yêu cầu: 75.00%
======================================================================

Báo cáo đã được lưu tại: docs/reports/cross_reference_report.json
```

### Bước 4: Tạo Issues cho Items Chưa hoàn thành

Khi phát hiện items chưa hoàn thành, tạo GitHub Issues:

1. Vào tab **Issues** trên GitHub
2. Click **New Issue**
3. Chọn template **"Hoàn thiện Item trong Checklist"**
4. Điền thông tin:
   - Giai đoạn
   - Mục cụ thể
   - Acceptance criteria
   - Tasks cần làm

### Bước 5: GitHub Actions Tự động

Hệ thống đã được cấu hình với GitHub Actions để tự động:

#### 5.1 Khi nào workflow chạy?

- **Push** vào branches: `main`, `master`, `develop`
- **Pull Request** vào các branches trên
- **Schedule**: Tự động vào thứ 2 hàng tuần lúc 9:00 AM
- **Manual**: Chạy thủ công từ GitHub Actions tab

#### 5.2 Các jobs được chạy

1. **check-completion**: Kiểm tra tỷ lệ hoàn thiện
2. **cross-reference**: Đối chiếu lý thuyết/thực tế
3. **code-quality**: Kiểm tra chất lượng code
4. **security-check**: Kiểm tra bảo mật
5. **documentation-check**: Kiểm tra tài liệu
6. **generate-report**: Tạo báo cáo tổng hợp

#### 5.3 Xem kết quả

1. Vào tab **Actions** trên GitHub
2. Chọn workflow run
3. Xem logs của từng job
4. Download artifacts (reports) nếu có

### Bước 6: Đánh giá Chất lượng

#### 6.1 Sử dụng Standards Document

Mở `docs/checklists/STANDARDS.md` và đánh giá từng hạng mục:

1. **Security**: Đánh giá OWASP Top 10 compliance
2. **Performance**: Đo response time, page load, etc.
3. **Maintainability**: Kiểm tra code quality, test coverage
4. **Architecture**: Review design patterns, principles
5. **Testing**: Đánh giá test coverage và quality
6. **DevOps**: Kiểm tra CI/CD, monitoring
7. **Compliance**: Đánh giá GDPR, accessibility, etc.

#### 6.2 Tính điểm

Điền điểm cho mỗi hạng mục (0-10) và tính điểm trọng số:

```
Điểm tổng = Σ(Điểm hạng mục × Trọng số)

Ví dụ:
- Security: 8/10 × 25% = 2.0
- Performance: 7/10 × 15% = 1.05
- ...
= Tổng: 7.5/10 (Tốt)
```

### Bước 7: Tạo Báo cáo Tổng hợp

#### 7.1 Sử dụng Template

Copy template báo cáo:

```bash
cp docs/templates/REPORT_TEMPLATE.md docs/reports/report_$(date +%Y%m%d).md
```

#### 7.2 Điền thông tin

Mở file báo cáo và điền:
1. Thông tin dự án
2. Tỷ lệ hoàn thiện từ Bước 2
3. Kết quả đối chiếu từ Bước 3
4. Điểm chất lượng từ Bước 6
5. Rủi ro và vấn đề
6. Đề xuất hành động

#### 7.3 Review và Share

1. Review báo cáo với team
2. Commit vào repository
3. Share link với stakeholders

---

## 3. Các Use Cases Thường gặp

### Use Case 1: Dự án mới bắt đầu

```bash
# 1. Clone repository
git clone <repo-url>
cd <repo-name>

# 2. Đọc tài liệu lý thuyết
cat docs/theory/THEORY.md

# 3. Review checklist
cat docs/checklists/CHECKLIST.md

# 4. Tạo plan và bắt đầu implement
# (Đánh dấu items trong checklist khi hoàn thành)

# 5. Định kỳ chạy scripts để track progress
python3 scripts/calculate_completion.py
```

### Use Case 2: Review dự án đang chạy

```bash
# 1. Pull latest code
git pull

# 2. Chạy cross-reference analysis
python3 scripts/cross_reference.py

# 3. Review kết quả và identify gaps
cat docs/reports/cross_reference_report.json

# 4. Update checklist dựa trên findings
vim docs/checklists/CHECKLIST.md

# 5. Tạo issues cho gaps
# (Sử dụng GitHub Issues templates)
```

### Use Case 3: Chuẩn bị release

```bash
# 1. Verify completion rate
python3 scripts/calculate_completion.py

# 2. Run full quality check (via GitHub Actions)
# Manually trigger workflow từ GitHub UI

# 3. Generate comprehensive report
cp docs/templates/REPORT_TEMPLATE.md docs/reports/release_report.md
# Fill in the report

# 4. Review with team
# 5. Fix any critical issues
# 6. Get approval
```

### Use Case 4: Audit và Compliance

```bash
# 1. Review standards document
cat docs/checklists/STANDARDS.md

# 2. Đánh giá từng hạng mục
# Fill in scores in STANDARDS.md

# 3. Generate audit report
# Use REPORT_TEMPLATE.md

# 4. Document any compliance gaps
# Create issues for fixes

# 5. Track remediation progress
```

---

## 4. Best Practices

### 4.1 Checklist Management

- **Update thường xuyên**: Đánh dấu items ngay khi hoàn thành
- **Specific**: Giữ items cụ thể và measurable
- **Review định kỳ**: Review checklist mỗi sprint/iteration
- **Team collaboration**: Cả team tham gia update

### 4.2 Quality Assessment

- **Objective metrics**: Sử dụng metrics đo lường được
- **Regular checks**: Chạy quality checks thường xuyên
- **Trend analysis**: Track xu hướng theo thời gian
- **Action-oriented**: Mỗi finding cần có action item

### 4.3 Reporting

- **Consistent format**: Sử dụng templates
- **Data-driven**: Base trên metrics thực tế
- **Actionable**: Include clear recommendations
- **Timely**: Report theo schedule

### 4.4 Automation

- **CI/CD integration**: Integrate checks vào pipeline
- **Automated alerts**: Setup alerts cho critical issues
- **Regular runs**: Schedule automatic checks
- **Artifact preservation**: Save reports và metrics

---

## 5. Troubleshooting

### Issue: Script không chạy được

**Solution:**
```bash
# Kiểm tra Python version
python3 --version  # Cần >= 3.6

# Cấp quyền execute
chmod +x scripts/*.py

# Chạy trực tiếp với Python
python3 scripts/calculate_completion.py
```

### Issue: GitHub Actions không trigger

**Solution:**
1. Check branch names trong workflow file
2. Verify quyền Actions được enable trong repo settings
3. Check workflow syntax với GitHub Actions validator

### Issue: Checklist không update được tỷ lệ

**Solution:**
- Đảm bảo format đúng: `- [ ]` cho unchecked, `- [x]` cho checked
- Phải có khoảng trắng giữa brackets
- Case-sensitive: [x] hoặc [X] đều được

### Issue: Cross-reference không phát hiện components

**Solution:**
- Script phát hiện dựa trên file patterns phổ biến
- Nếu dự án dùng structure khác, customize script
- Thêm patterns vào `backend_indicators`, `frontend_indicators`, etc.

---

## 6. Customization

### 6.1 Customize Checklist

Thêm/bớt items trong `docs/checklists/CHECKLIST.md` theo nhu cầu dự án:

```markdown
## 8. Custom Section cho Dự án

### 8.1 Specific Requirement
- [ ] Custom item 1
- [ ] Custom item 2
```

### 6.2 Customize Standards

Điều chỉnh trọng số trong `docs/checklists/STANDARDS.md`:

```markdown
| Hạng mục | Trọng số |
|----------|----------|
| Security | 30%      |  # Tăng nếu dự án cần security cao
| Performance | 25%   |  # Tăng nếu performance critical
```

### 6.3 Customize Scripts

Edit scripts trong `scripts/` để:
- Thêm checks mới
- Customize output format
- Integrate với tools khác
- Add email notifications

### 6.4 Customize Workflows

Edit `.github/workflows/project_review.yml` để:
- Thêm/bớt jobs
- Thay đổi schedule
- Add notifications (Slack, email, etc.)
- Integrate với third-party tools

---

## 7. Integration với Tools khác

### 7.1 SonarQube

```yaml
# Thêm vào workflow
- name: SonarQube Scan
  uses: sonarsource/sonarqube-scan-action@master
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### 7.2 Dependency Scanning

```yaml
- name: Run Snyk
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### 7.3 Performance Testing

```yaml
- name: Lighthouse CI
  uses: treosh/lighthouse-ci-action@v9
  with:
    urls: |
      https://your-app.com
```

---

## 8. FAQ

**Q: Tỷ lệ hoàn thiện bao nhiêu là đủ để release?**
A: Tối thiểu 95% cho production release. 100% là ideal.

**Q: Có cần chạy scripts mỗi ngày không?**
A: Không bắt buộc. Chạy khi có changes hoặc theo schedule (ví dụ: weekly).

**Q: Script có hoạt động với ngôn ngữ nào?**
A: Scripts hiện tại detect các patterns phổ biến cho Node.js, Python, .NET, Go, Java, PHP.

**Q: Có thể dùng cho microservices không?**
A: Có. Chạy scripts cho từng service và aggregate results.

**Q: Làm sao để track progress theo thời gian?**
A: Commit reports vào repository hoặc integrate với analytics tools.

---

## 9. Support

Nếu gặp vấn đề:
1. Check troubleshooting section
2. Review documentation
3. Create issue sử dụng template
4. Contact team lead

---

## 10. Contributing

Để contribute vào hệ thống:
1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests nếu applicable
5. Submit pull request
6. Ensure CI passes

---

**Cập nhật lần cuối:** 2024
**Phiên bản:** 1.0
