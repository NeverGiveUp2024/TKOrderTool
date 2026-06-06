; ================================
; 专业版 Inno Setup
; ================================

[Setup]
AppName=达人订单统计工具
AppVersion=1.0
DefaultDirName={autopf}\达人订单统计工具
DefaultGroupName=达人订单统计工具
OutputBaseFilename=达人订单统计工具_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
DisableDirPage=no
DisableProgramGroupPage=yes

; ================================
; 文件复制
; ================================

[Files]

Source: "gui.exe"; DestDir: "{app}"; Flags: ignoreversion

; data 目录（关键）
Source: "data\orders\*"; DestDir: "{app}\data\orders"; Flags: recursesubdirs createallsubdirs
Source: "data\sku_mapping.xlsx"; DestDir: "{app}\data"; Flags: ignoreversion
Source: "data\influencer_mapping.xlsx"; DestDir: "{app}\data"; Flags: ignoreversion

; 输出目录（可空文件夹初始化）
Source: "cleaned_orders\*"; DestDir: "{app}\cleaned_orders"; Flags: recursesubdirs createallsubdirs
Source: "merged_orders\*"; DestDir: "{app}\merged_orders"; Flags: recursesubdirs createallsubdirs

; ================================
; 创建文件夹（防止空目录丢失）
; ================================

[Dirs]
Name: "{app}\data"
Name: "{app}\data\orders"
Name: "{app}\cleaned_orders"
Name: "{app}\merged_orders"

; ================================
; 快捷方式
; ================================

[Icons]
Name: "{group}\达人订单统计工具"; Filename: "{app}\gui.exe"
Name: "{commondesktop}\达人订单统计工具"; Filename: "{app}\gui.exe"

; ================================
; 安装后初始化（重点）
; ================================

[Run]
Filename: "{cmd}"; Parameters: "/C if not exist ""{app}\data\orders"" mkdir ""{app}\data\orders"""; Flags: runhidden
Filename: "{cmd}"; Parameters: "/C if not exist ""{app}\cleaned_orders"" mkdir ""{app}\cleaned_orders"""; Flags: runhidden
Filename: "{cmd}"; Parameters: "/C if not exist ""{app}\merged_orders"" mkdir ""{app}\merged_orders"""; Flags: runhidden