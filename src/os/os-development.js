#!/usr/bin/env node
/**
 * EHB OS Development Environment
 * Supports: Kernel Development, Device Drivers, System Programming
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const ora = require('ora');
const { spawn } = require('child_process');

class OSDevelopmentEnvironment {
  constructor() {
    this.templates = {
      'kernel-module': {
        name: 'Linux Kernel Module',
        description: 'Basic kernel module template',
        language: 'c',
      },
      'device-driver': {
        name: 'Device Driver',
        description: 'Hardware device driver template',
        language: 'c',
      },
      filesystem: {
        name: 'Custom File System',
        description: 'File system implementation template',
        language: 'c',
      },
      'network-stack': {
        name: 'Network Stack',
        description: 'Network protocol implementation',
        language: 'c',
      },
      'rust-os': {
        name: 'Rust OS',
        description: 'Operating system in Rust',
        language: 'rust',
      },
    };

    this.projects = new Map();
    this.buildTools = {
      c: ['gcc', 'make', 'cmake'],
      rust: ['cargo', 'rustc'],
      assembly: ['nasm', 'gcc'],
    };
  }

  async initialize() {
    console.log(chalk.blue('💻 Initializing OS Development Environment...'));

    await this.checkBuildTools();
    await this.loadTemplates();
    await this.setupQEMU();

    console.log(chalk.green('✅ OS Development environment ready!'));
  }

  async checkBuildTools() {
    const spinner = ora('Checking build tools...').start();

    try {
      const tools = ['gcc', 'make', 'rustc', 'cargo', 'qemu-system-x86_64'];
      const availableTools = [];

      for (const tool of tools) {
        try {
          await this.checkTool(tool);
          availableTools.push(tool);
        } catch (error) {
          console.log(chalk.yellow(`⚠️  ${tool} not found`));
        }
      }

      if (availableTools.length > 0) {
        spinner.succeed(`Build tools available: ${availableTools.join(', ')}`);
      } else {
        spinner.warn('No build tools found. Please install development tools.');
      }
    } catch (error) {
      spinner.fail('Failed to check build tools');
    }
  }

  async checkTool(tool) {
    return new Promise((resolve, reject) => {
      const process = spawn(tool, ['--version'], { stdio: 'ignore' });
      process.on('close', (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject();
        }
      });
    });
  }

  async loadTemplates() {
    this.templates = {
      'kernel-module': {
        name: 'Linux Kernel Module',
        description: 'Basic kernel module template',
        language: 'c',
        files: [
          {
            name: 'module.c',
            content: this.getKernelModuleTemplate(),
          },
          {
            name: 'Makefile',
            content: this.getKernelMakefileTemplate(),
          },
          {
            name: 'README.md',
            content: this.getKernelReadmeTemplate(),
          },
        ],
      },
      'device-driver': {
        name: 'Device Driver',
        description: 'Hardware device driver template',
        language: 'c',
        files: [
          {
            name: 'driver.c',
            content: this.getDeviceDriverTemplate(),
          },
          {
            name: 'Makefile',
            content: this.getDriverMakefileTemplate(),
          },
        ],
      },
      'rust-os': {
        name: 'Rust OS',
        description: 'Operating system in Rust',
        language: 'rust',
        files: [
          {
            name: 'Cargo.toml',
            content: this.getRustOSTemplate(),
          },
          {
            name: 'src/main.rs',
            content: this.getRustOSMainTemplate(),
          },
        ],
      },
    };
  }

  getKernelModuleTemplate() {
    return `#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("EHB AI Dev Agent");
MODULE_DESCRIPTION("A simple kernel module");
MODULE_VERSION("1.0");

static int __init hello_init(void) {
    printk(KERN_INFO "Hello, World! Module loaded.\\n");
    return 0;
}

static void __exit hello_exit(void) {
    printk(KERN_INFO "Goodbye, World! Module unloaded.\\n");
}

module_init(hello_init);
module_exit(hello_exit);`;
  }

  getKernelMakefileTemplate() {
    return `obj-m += module.o

all:
	make -C /lib/modules/\$(shell uname -r)/build M=\$(PWD) modules

clean:
	make -C /lib/modules/\$(shell uname -r)/build M=\$(PWD) clean

install:
	sudo insmod module.ko

uninstall:
	sudo rmmod module`;
  }

  getDeviceDriverTemplate() {
    return `#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/device.h>

#define DEVICE_NAME "ehb_device"
#define CLASS_NAME "ehb_class"

MODULE_LICENSE("GPL");
MODULE_AUTHOR("EHB AI Dev Agent");
MODULE_DESCRIPTION("A simple device driver");
MODULE_VERSION("1.0");

static int major_number;
static struct class* ehb_class = NULL;
static struct device* ehb_device = NULL;

static int dev_open(struct inode *inodep, struct file *filep) {
    printk(KERN_INFO "EHB Device opened\\n");
    return 0;
}

static ssize_t dev_read(struct file *filep, char *buffer, size_t len, loff_t *offset) {
    int error_count = 0;
    error_count = copy_to_user(buffer, "Hello from EHB Device!\\n", 25);
    
    if (error_count == 0) {
        printk(KERN_INFO "EHB Device: Sent %d characters to user\\n", 25);
        return 25;
    } else {
        printk(KERN_INFO "EHB Device: Failed to send %d characters to user\\n", error_count);
        return -EFAULT;
    }
}

static ssize_t dev_write(struct file *filep, const char *buffer, size_t len, loff_t *offset) {
    printk(KERN_INFO "EHB Device: Received %zu characters from user\\n", len);
    return len;
}

static int dev_release(struct inode *inodep, struct file *filep) {
    printk(KERN_INFO "EHB Device closed\\n");
    return 0;
}

static struct file_operations fops = {
    .open = dev_open,
    .read = dev_read,
    .write = dev_write,
    .release = dev_release,
};

static int __init driver_entry(void) {
    printk(KERN_INFO "EHB Device Driver: Initializing\\n");
    
    major_number = register_chrdev(0, DEVICE_NAME, &fops);
    if (major_number < 0) {
        printk(KERN_ALERT "EHB Device Driver failed to register a major number\\n");
        return major_number;
    }
    
    ehb_class = class_create(THIS_MODULE, CLASS_NAME);
    if (IS_ERR(ehb_class)) {
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "Failed to register device class\\n");
        return PTR_ERR(ehb_class);
    }
    
    ehb_device = device_create(ehb_class, NULL, MKDEV(major_number, 0), NULL, DEVICE_NAME);
    if (IS_ERR(ehb_device)) {
        class_destroy(ehb_class);
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "Failed to create the device\\n");
        return PTR_ERR(ehb_device);
    }
    
    printk(KERN_INFO "EHB Device Driver: Device class created correctly\\n");
    return 0;
}

static void __exit driver_exit(void) {
    device_destroy(ehb_class, MKDEV(major_number, 0));
    class_unregister(ehb_class);
    class_destroy(ehb_class);
    unregister_chrdev(major_number, DEVICE_NAME);
    printk(KERN_INFO "EHB Device Driver: Goodbye!\\n");
}

module_init(driver_entry);
module_exit(driver_exit);`;
  }

  getRustOSTemplate() {
    return `[package]
name = "ehb-os"
version = "0.1.0"
edition = "2021"

[dependencies]
bootloader = "0.9"
x86_64 = "0.14"

[package.metadata.bootimage]
test-args = [
    "--test-threads=1",
    "--nocapture"
]
test-timeout = 300
test-timeout-unit = "s"

[dependencies.bootimage]
version = "0.11"
optional = true

[profile.dev]
opt-level = 1

[profile.release]
opt-level = 3`;
  }

  getRustOSMainTemplate() {
    return `#![no_std]
#![no_main]
#![feature(custom_test_frameworks)]
#![test_runner(blog_os::test_runner)]
#![reexport_test_harness_main = "test_main"]

use core::panic::PanicInfo;
use blog_os::{println, print};

#[no_mangle]
pub extern "C" fn _start() -> ! {
    println!("Hello World{}", "!");
    blog_os::hlt_loop();
}

#[cfg(not(test))]
#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    println!("{}", info);
    blog_os::hlt_loop();
}

#[cfg(test)]
#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    blog_os::test_panic_handler(info)
}

#[test_case]
fn trivial_assertion() {
    print!("trivial assertion... ");
    assert_eq!(1, 1);
    println!("[ok]");
}`;
  }

  async setupQEMU() {
    const spinner = ora('Setting up QEMU for OS testing...').start();

    try {
      // Check if QEMU is available
      await this.checkTool('qemu-system-x86_64');
      spinner.succeed('QEMU is available for OS testing');
    } catch (error) {
      spinner.warn('QEMU not found. OS testing will be limited.');
    }
  }

  async createProject(projectName, templateType) {
    const spinner = ora(
      `Creating ${templateType} project: ${projectName}`
    ).start();

    try {
      const projectPath = path.join('projects', projectName);
      await fs.ensureDir(projectPath);

      const template = this.templates[templateType];
      if (!template) {
        throw new Error(`Template ${templateType} not found`);
      }

      // Create project structure
      if (template.language === 'rust') {
        await fs.ensureDir(path.join(projectPath, 'src'));
      }

      // Copy template files
      for (const file of template.files) {
        const filePath = path.join(projectPath, file.name);
        await fs.ensureDir(path.dirname(filePath));
        await fs.writeFile(filePath, file.content);
      }

      // Create additional files based on language
      if (template.language === 'c') {
        await this.createCProjectFiles(projectPath, projectName);
      } else if (template.language === 'rust') {
        await this.createRustProjectFiles(projectPath, projectName);
      }

      this.projects.set(projectName, {
        path: projectPath,
        type: templateType,
        language: template.language,
        createdAt: new Date().toISOString(),
        status: 'created',
      });

      spinner.succeed(`OS project ${projectName} created successfully!`);
      return projectPath;
    } catch (error) {
      spinner.fail(`Failed to create project: ${error.message}`);
      throw error;
    }
  }

  async createCProjectFiles(projectPath, projectName) {
    // Create .gitignore
    const gitignore = `*.o
*.ko
*.mod.c
*.mod
*.cmd
.tmp_versions/
*.symvers
*.order
*.d
*.dwo
*.ko.cmd
*.mod.cmd
*.o.cmd
*.o.dwo
*.ko.dwo
*.mod.dwo
*.cmd.dwo
*.symvers.dwo
*.order.dwo
*.d.dwo
*.dwo.dwo
*.ko.cmd.dwo
*.mod.cmd.dwo
*.o.cmd.dwo
*.o.dwo.dwo
*.ko.dwo.dwo
*.mod.dwo.dwo
*.cmd.dwo.dwo
*.symvers.dwo.dwo
*.order.dwo.dwo
*.d.dwo.dwo
*.dwo.dwo.dwo`;

    await fs.writeFile(path.join(projectPath, '.gitignore'), gitignore);
  }

  async createRustProjectFiles(projectPath, projectName) {
    // Create .cargo/config.toml for Rust OS
    const cargoConfig = `[unstable]
build-std-features = ["compiler-builtins-mem"]
build-std = ["core", "compiler_builtins"]

[target.'cfg(target_os = "none")']
runner = "bootimage runner"
rustflags = [
    "-C", "link-arg=--image-base=0x80000000",
]`;

    await fs.ensureDir(path.join(projectPath, '.cargo'));
    await fs.writeFile(
      path.join(projectPath, '.cargo/config.toml'),
      cargoConfig
    );
  }

  async buildProject(projectName) {
    const project = this.projects.get(projectName);
    if (!project) {
      throw new Error(`Project ${projectName} not found`);
    }

    const spinner = ora(`Building ${projectName}...`).start();

    try {
      const projectPath = project.path;

      if (project.language === 'c') {
        // Build C project
        await this.buildCProject(projectPath);
      } else if (project.language === 'rust') {
        // Build Rust project
        await this.buildRustProject(projectPath);
      }

      project.status = 'built';
      spinner.succeed(`${projectName} built successfully!`);
    } catch (error) {
      project.status = 'build_failed';
      spinner.fail(`Failed to build ${projectName}: ${error.message}`);
      throw error;
    }
  }

  async buildCProject(projectPath) {
    return new Promise((resolve, reject) => {
      const process = spawn('make', [], { cwd: projectPath });

      process.stdout.on('data', (data) => {
        console.log(chalk.blue(data.toString()));
      });

      process.stderr.on('data', (data) => {
        console.log(chalk.red(data.toString()));
      });

      process.on('close', (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject(new Error(`Build failed with code ${code}`));
        }
      });
    });
  }

  async buildRustProject(projectPath) {
    return new Promise((resolve, reject) => {
      const process = spawn('cargo', ['build'], { cwd: projectPath });

      process.stdout.on('data', (data) => {
        console.log(chalk.blue(data.toString()));
      });

      process.stderr.on('data', (data) => {
        console.log(chalk.red(data.toString()));
      });

      process.on('close', (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject(new Error(`Build failed with code ${code}`));
        }
      });
    });
  }

  async testProject(projectName) {
    const project = this.projects.get(projectName);
    if (!project) {
      throw new Error(`Project ${projectName} not found`);
    }

    const spinner = ora(`Testing ${projectName}...`).start();

    try {
      const projectPath = project.path;

      if (project.language === 'c') {
        await this.testCProject(projectPath);
      } else if (project.language === 'rust') {
        await this.testRustProject(projectPath);
      }

      spinner.succeed(`${projectName} tests passed!`);
    } catch (error) {
      spinner.fail(`Tests failed for ${projectName}: ${error.message}`);
      throw error;
    }
  }

  async testCProject(projectPath) {
    return new Promise((resolve, reject) => {
      const process = spawn('make', ['test'], { cwd: projectPath });

      process.stdout.on('data', (data) => {
        console.log(chalk.green(data.toString()));
      });

      process.stderr.on('data', (data) => {
        console.log(chalk.red(data.toString()));
      });

      process.on('close', (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject(new Error(`Tests failed with code ${code}`));
        }
      });
    });
  }

  async testRustProject(projectPath) {
    return new Promise((resolve, reject) => {
      const process = spawn('cargo', ['test'], { cwd: projectPath });

      process.stdout.on('data', (data) => {
        console.log(chalk.green(data.toString()));
      });

      process.stderr.on('data', (data) => {
        console.log(chalk.red(data.toString()));
      });

      process.on('close', (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject(new Error(`Tests failed with code ${code}`));
        }
      });
    });
  }

  getProjectInfo() {
    return Array.from(this.projects.entries()).map(([name, project]) => ({
      name,
      type: project.type,
      language: project.language,
      status: project.status,
      createdAt: project.createdAt,
      path: project.path,
    }));
  }

  getTemplates() {
    return Object.entries(this.templates).map(([key, template]) => ({
      key,
      name: template.name,
      description: template.description,
      language: template.language,
    }));
  }
}

// Export for use in main agent
module.exports = OSDevelopmentEnvironment;

// Start if run directly
if (require.main === module) {
  const env = new OSDevelopmentEnvironment();
  env
    .initialize()
    .then(() => {
      console.log(chalk.green('💻 OS Development Environment is ready!'));
      console.log(chalk.blue('Available templates:'));
      for (const template of env.getTemplates()) {
        console.log(
          chalk.cyan(
            `  - ${template.key}: ${template.name} (${template.language})`
          )
        );
      }
    })
    .catch(console.error);
}
